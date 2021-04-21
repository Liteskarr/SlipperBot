"""
Страница ввода ФИО.
"""

import requests

from abstractions.ipage import IPage
from abstractions.message import Message
from config import cfg
from pages.region_input import RegionInputPage


def test_fio(fio: str) -> bool:
    return bool(fio) and len(fio.split()) == 3


page_starting_text = """Введите ваше ФИО."""

error_text = """Некорректные данные. Если это не так, то обратитесь к администратору!"""


class NameInputPage(IPage):
    def handle_starting(self):
        self._bot.send_message(Message(page_starting_text))

    def handle_new_message(self, message: Message):
        if test_fio(message.text):
            requests.put(cfg.get('API', 'API_ADDRESS') + f'/student/{self._bot.get_current_user()}',
                         {'name': message.text})
            self.on_page_changing.notify(RegionInputPage(self._bot))
        else:
            self._bot.send_message(Message(error_text))
