"""
Страница, приветствующая пользователя.
"""

import requests

from abstractions.button import Button, ButtonColor
from abstractions.ipage import IPage
from abstractions.keyboard import Keyboard
from abstractions.message import Message
from config import cfg
from pages.registration_starting import RegistrationStartingPage

default_keyboard = Keyboard(
    ((0, 0), Button('Привет!', ButtonColor.POSITIVE))
)


class IntroductionPage(IPage):
    def handle_starting(self):
        requests.post(cfg.get('API', 'API_ADDRESS') + f'/student/{self._bot.get_current_user()}',
                      {'registered': False, 'vk_id': self._bot.get_current_user()})

    def handle_new_message(self, message: Message):
        self.on_page_changing.notify(RegistrationStartingPage(self._bot))
