"""
Класс, управляющий пользовательскими страницами.
"""

import pickle
from typing import Union

from abstractions.button import Button
from abstractions.ibot import IBot
from abstractions.ipage import IPage
from abstractions.message import Message
from abstractions.pages_container import PagesContainer


class PagesManager:
    def __init__(self, pages_container: PagesContainer, bot: IBot, default_page_type: type):
        self._pages_container = pages_container
        self._bot: IBot = bot
        self._bot.on_new_user.add(self.handle_new_user)
        self._bot.on_new_message.add(self.handle_new_message)
        self._bot.on_button_click.add(self.handle_button_click)
        self._bot.on_event.add(self.handle_event)
        self._current_user: Union[str, None] = None
        self._current_page: Union[IPage, None] = None
        self._default_page: type = default_page_type

    def handle_new_message(self, message: Message):
        self._current_page.handle_new_message(message)

    def handle_button_click(self, button: Button):
        self._current_page.handle_button_click(button)

    def handle_new_user(self, user_id: str):
        self._dump_user()
        self._current_user = user_id
        self._load_user(user_id)

    def handle_event(self, event_data: dict):
        self._current_page.handle_event(event_data)

    def handle_page_changing(self, page: IPage, with_starting: bool = True):
        if self._current_page is not None:
            self._current_page.on_page_changing.delete(id(self.handle_page_changing))
        self._current_page = page
        self._current_page._bot = self._bot
        self._current_page.on_page_changing.add(self.handle_page_changing)
        if with_starting:
            self._current_page.handle_starting()

    def _load_user(self, user_id: str):
        if self._pages_container.contains(user_id):
            self.handle_page_changing(pickle.loads(self._pages_container.get(user_id)), with_starting=False)
        else:
            self.handle_page_changing(self._default_page(self._bot), with_starting=True)

    def _dump_user(self):
        if self._current_page is None:
            return
        self._pages_container.set(str(self._current_user), pickle.dumps(self._current_page))
        self._current_page = None
