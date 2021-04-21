"""
Страница завершения регистрации.
"""

from abstractions.ipage import IPage
from abstractions.message import Message

from pages.notifications_handler import NotificationsHandlerPage

registration_ending_text = """Вы успешно завершили регистрацию!"""


class RegistrationEndingPage(IPage):
    def handle_starting(self):
        self._bot.send_message(Message(registration_ending_text))
        self.on_page_changing.notify(NotificationsHandlerPage(self._bot))
