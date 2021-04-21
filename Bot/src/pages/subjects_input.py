"""
Страница выбора предметов обучения.
"""

import requests

from abstractions.button import Button, ButtonColor
from abstractions.ibot import IBot
from abstractions.ipage import IPage
from abstractions.keyboard import Keyboard
from abstractions.message import Message
from config import cfg
from pages.registration_ending import RegistrationEndingPage

adding_button = Button('Добавить', ButtonColor.POSITIVE)
deleting_button = Button('Удалить', ButtonColor.NEGATIVE)
finishing_button = Button('Завершить', ButtonColor.PRIMARY)

local_menu = Keyboard(
    ((0, 0), adding_button),
    ((0, 1), deleting_button),
    ((0, 2), finishing_button)
)

page_starting_text = """Вам предлагается выбрать несколько интересующих вас предметов."""

subjects_list_prefix = """Выбранные предметы:"""

subjects_does_not_chosen_text = """Вы не выбрали ничего."""

subject_does_not_exist_text = """Такого предмета нет в базе данных!"""

subject_added_text = """Предмет успешно добавлен!"""

subject_deleted_text = """Предмет успешно добавлен!"""

keyboard_message = """Обратите внимание на клавиатуру."""

adding_state_text = """Введите название интересующего предмета."""

ADDING_STATE = 1
DELETING_STATE = 2
MENU_STATE = 3


class SubjectsInputPage(IPage):
    def __init__(self, bot: IBot):
        super().__init__(bot)
        self._subjects = []
        self._state = MENU_STATE

    def try_to_add_subject(self, subject_name: str):
        subject_name = subject_name.lower()
        subjects = requests.get(cfg.get('API', 'API_ADDRESS') + '/subjects').json()
        for subject in subjects['subjects']:
            if subject['name'] == subject_name and subject not in self._subjects:
                self._subjects.append(subject)
                return True
        return False

    def delete_subject(self, subject_name: str):
        for subject in self._subjects:
            if subject['name'] == subject_name:
                self._subjects.remove(subject)
                return

    def handle_starting(self):
        self._bot.send_message(Message(page_starting_text))
        self._bot.set_keyboard(local_menu, message=keyboard_message)

    def handle_new_message(self, message: Message):
        if self._state == MENU_STATE:
            if message.text == adding_button.text:
                self._bot.send_message(Message(adding_state_text))
                self._state = ADDING_STATE
            elif message.text == deleting_button.text:
                self._state = DELETING_STATE
            elif message.text == finishing_button.text:
                requests.put(cfg.get('API', 'API_ADDRESS') + f'/student/{self._bot.get_current_user()}',
                             {'subjects': str(self._subjects)})
                self.on_page_changing.notify(RegistrationEndingPage(self._bot))
                return
            else:
                self._bot.set_keyboard(local_menu, message=keyboard_message)
        elif self._state == ADDING_STATE:
            if not self.try_to_add_subject(message.text):
                self._bot.send_message(Message(subject_does_not_exist_text))
            else:
                self._bot.send_message(Message(subject_added_text))
            self._bot.set_keyboard(local_menu, message=keyboard_message)
            self._state = MENU_STATE
        elif self._state == DELETING_STATE:
            self.delete_subject(message.text)
            self._bot.send_message(Message(subject_deleted_text))
            self._bot.set_keyboard(local_menu, message=keyboard_message)
            self._state = MENU_STATE
        if len(self._subjects):
            self._bot.send_message(Message(
                f'{subjects_list_prefix} {"; ".join(map(lambda x: x["name"], self._subjects))}.'
            ))
        else:
            self._bot.send_message(Message(subjects_does_not_chosen_text))

    def __getstate__(self):
        return {
            '_subjects': self._subjects,
            '_state': self._state
        }
