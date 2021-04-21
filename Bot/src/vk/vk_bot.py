"""
Реализация интерфейса IBot для бота ВКонтакте.
"""

from datetime import datetime
from random import getrandbits
from typing import NoReturn, Union

import requests
import schedule
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from abstractions.button import ButtonColor
from abstractions.ibot import IBot
from abstractions.keyboard import Keyboard
from abstractions.message import Message
from config import cfg

VK_BUTTON_COLOR = {
    ButtonColor.PRIMARY: VkKeyboardColor.PRIMARY,
    ButtonColor.SECONDARY: VkKeyboardColor.SECONDARY,
    ButtonColor.NEGATIVE: VkKeyboardColor.NEGATIVE,
    ButtonColor.POSITIVE: VkKeyboardColor.POSITIVE
}


class VkBot(IBot):
    def __init__(self, token: str, group_id: int):
        super().__init__()
        self._api = VkApi(token=token)
        self._longpoll = VkBotLongPoll(self._api, group_id=group_id)
        self._longpoll.wait = 0
        self._current_user: Union[int, None] = None

    def change_user(self, user_id: int):
        self._current_user = user_id
        self.on_new_user.notify(user_id)

    def send_message(self, message: Message):
        if self._current_user is None:
            return
        self._api.method('messages.send', values={
            'peer_id': self._current_user,
            'message': message.text,
            'random_id': int(getrandbits(32))
        })

    def set_keyboard(self, keyboard: Keyboard, message: str = 'keyboard'):
        vk_keyboard = VkKeyboard(True)
        current_line = 1
        for pos, button in keyboard.all():
            row, column = pos
            if row + 1 < current_line:
                current_line += 1
                vk_keyboard.add_line()
            vk_keyboard.add_button(button.text, VK_BUTTON_COLOR[button.color])
        self._api.method('messages.send', values={
            'peer_id': self._current_user,
            'random_id': int(getrandbits(32)),
            'keyboard': vk_keyboard.get_keyboard(),
            'message': message
        })

    def get_current_user(self):
        return self._current_user

    def handle_server_event(self):
        last_notification_id = int(cfg.get('SETTINGS', 'LAST_ID'))
        data = requests.get(cfg.get('API', 'API_ADDRESS') + f'/notifications/{last_notification_id}').json()
        last_notification_id = data['meta']['last_id']
        cfg.set('SETTINGS', 'LAST_ID', str(last_notification_id))
        cfg.write(open('settings.cfg', 'w'))
        for student, notifications in data['students'].items():
            self.change_user(int(student))
            for student_data in notifications:
                current_contest = None
                for contest, contest_data in data['contests'].items():
                    if contest == str(student_data['contest']):
                        current_contest = contest_data
                        current_contest['id'] = contest
                        break
                current_stage = None
                for stage, stage_data in data['stages'].items():
                    if stage == str(student_data['stage']):
                        current_stage = stage_data
                        current_stage['id'] = stage
                        break
                self.on_event.notify({
                    'contest': current_contest,
                    'stage': current_stage,
                    'student': student
                })

    def run(self) -> NoReturn:
        print('Бот начал работу!')
        schedule.every(5).seconds.do(self.handle_server_event)
        while True:
            try:
                for event in self._longpoll.check():
                    if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
                        self.change_user(event.message.from_id)
                        self.on_new_message.notify(Message(event.message.get('text', '')))
                schedule.run_pending()
            except requests.ConnectionError:
                print(f'{datetime.now()}: Не удается подключиться к серверу!')
