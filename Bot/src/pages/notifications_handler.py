"""
Страница приема уведомлений.
"""

from collections import deque

import requests

from abstractions.button import Button, ButtonColor
from abstractions.ipage import IPage
from abstractions.keyboard import Keyboard
from abstractions.message import Message
from config import cfg

new_notification_pattern = """
Напоминание о предстоящем мероприятии!
Мероприятие: {0}
Этап мероприятия: {1}

Дата начала: {2}.
Дата окончания: {3}.

Описание мероприятия: {4}

Описание этапа: {5}
"""

page_starting_text = """=== Начало приема напоминаний ==="""

command_error_text = """Не существует такой опции!"""

empty_event_queue_text = """На данный момент нет напоминаний!"""

ok_text = """Принято!"""

confirm_button = Button('Принято!', ButtonColor.POSITIVE)
refuse_button = Button('Не напоминать.', ButtonColor.NEGATIVE)

local_menu = Keyboard(
    ((0, 0), confirm_button),
    ((0, 1), refuse_button)
)


class NotificationsHandlerPage(IPage):
    def handle_starting(self):
        self._events_queue = deque()
        self._offered = False
        self.current_event = {}
        self._bot.send_message(Message(page_starting_text))

    def try_offer(self):
        if len(self._events_queue) and not self._offered:
            self._offered = True
            self.offer_front_event()

    def offer_front_event(self):
        event = self._events_queue.popleft()
        self.current_event = event
        self._bot.send_message(Message(new_notification_pattern.format(
            event['contest']['name'],
            event['stage']['name'],
            event['stage']['starting_date'],
            event['stage']['ending_date'],
            event['contest']['description'],
            event['stage']['description']
        )))
        self._bot.set_keyboard(local_menu, message='Выберите один из предложенных вариантов.')

    def handle_new_message(self, message: Message):
        if self._offered:
            if message.text == confirm_button.text:
                self._offered = False
                self.try_offer()
            elif message.text == refuse_button.text:
                requests.post(cfg.get('API', 'API_ADDRESS') + f'/student_declines/{self._bot.get_current_user()}',
                              {'contest_id': self.current_event['contest']['id']})
                self._bot.send_message(Message(ok_text))
                self._offered = False
                self.try_offer()
            else:
                self._bot.send_message(Message(command_error_text))
        else:
            self._bot.send_message(Message(empty_event_queue_text))

    def handle_event(self, event_data: dict):
        self._events_queue.append(event_data)
        self.try_offer()

    def __getstate__(self):
        return {
            '_events_queue': self._events_queue,
            '_offered': self._offered,
            'current_event': self.current_event
        }
