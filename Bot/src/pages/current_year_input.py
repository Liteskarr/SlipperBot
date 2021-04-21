"""
Страница ввода текущего класса обучения.
"""

import requests

from abstractions.ipage import IPage
from abstractions.message import Message
from config import cfg
from pages.target_year_input import TargetYearInputPage

years = list(range(1, 12))


def test_current_year(year: str):
    try:
        return int(year) in years
    except Exception:
        return False


page_starting_text = """Введите текущий класс обучения."""

error_text = """Некорректный класс!"""


class CurrentYearInputPage(IPage):
    def handle_starting(self):
        self._bot.send_message(Message(page_starting_text))

    def handle_new_message(self, message: Message):
        if test_current_year(message.text):
            requests.put(cfg.get('API', 'API_ADDRESS') + f'/student/{self._bot.get_current_user()}',
                         {'current_year': int(message.text)})
            self.on_page_changing.notify(TargetYearInputPage(self._bot))
        else:
            self._bot.send_message(Message(error_text))
