"""
Страница ввода региона пользователя.
"""

import requests

from abstractions.ipage import IPage
from abstractions.message import Message
from config import cfg
from pages.current_year_input import CurrentYearInputPage


def test_region_code(region_code: int):
    return 1 <= region_code <= 97


page_starting_text = """Введите код вашего региона."""

error_text = """Некорректный код региона!"""


class RegionInputPage(IPage):
    def handle_starting(self):
        self._bot.send_message(Message(page_starting_text))

    def handle_new_message(self, message: Message):
        if test_region_code(int(message.text)):
            requests.put(cfg.get('API', 'API_ADDRESS') + f'/student/{self._bot.get_current_user()}',
                         {'region': message.text})
            self.on_page_changing.notify(CurrentYearInputPage(self._bot))
        else:
            self._bot.send_message(Message(error_text))
