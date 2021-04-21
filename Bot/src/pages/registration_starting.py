"""
Страница начала регистрации.
"""

from abstractions.ipage import IPage
from abstractions.message import Message

from pages.name_input import NameInputPage

introduction_text = """
Перед началом работы следует пройти регистрацию в системе.
"""


class RegistrationStartingPage(IPage):
    def handle_starting(self):
        self._bot.send_message(Message(introduction_text))
        self.on_page_changing.notify(NameInputPage(self._bot))
