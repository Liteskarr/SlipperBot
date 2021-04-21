"""
Страница выбора интересующего года обучения.
"""

import requests

from abstractions.ipage import IPage
from abstractions.message import Message
from config import cfg
from pages.subjects_input import SubjectsInputPage

years = list(range(1, 12))


def test_target_year(year: str, student_vk: str):
    data = requests.get(cfg.get('API', 'API_ADDRESS') + f'/student/{student_vk}').json()
    return int(data['current_year']) <= int(year) and int(year) in years


page_starting_text = """Введите интересующий класс обучения. Вы не можете выбрать класс, который уже завершили."""

error_text = """Некорректный ввод!"""


class TargetYearInputPage(IPage):
    def handle_starting(self):
        self._bot.send_message(Message(page_starting_text))

    def handle_new_message(self, message: Message):
        if test_target_year(message.text, self._bot.get_current_user()):
            requests.put(cfg.get('API', 'API_ADDRESS') + f'/student/{self._bot.get_current_user()}',
                         {'target_year': message.text})
            self.on_page_changing.notify(SubjectsInputPage(self._bot))
        else:
            self._bot.send_message(Message(error_text))
