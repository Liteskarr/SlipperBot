"""
Абстракция страницы бота.
"""

from utilities.signal import Signal

from abstractions.ibot import IBot
from abstractions.message import Message
from abstractions.button import Button


class IPage:
    def __init__(self, bot: IBot):
        self.on_page_changing = Signal(IPage)
        self._bot = bot

    def handle_starting(self):
        pass

    def handle_new_message(self, message: Message):
        pass

    def handle_button_click(self, button: Button):
        pass

    def handle_event(self, event_data: dict):
        pass

    def __getstate__(self):
        return {}

    def __setstate__(self, state):
        self.on_page_changing = Signal(IPage)
        vars(self).update(state)
