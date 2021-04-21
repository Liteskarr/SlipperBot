"""
Абстракция бота.
"""

from typing import NoReturn

from utilities.signal import Signal

from abstractions.message import Message
from abstractions.keyboard import Keyboard


class IBot:
    def __init__(self):
        self.on_new_user = Signal(int)
        self.on_new_message = Signal(Message)
        self.on_button_click = Signal()
        self.on_event = Signal()

    def send_message(self, message: Message):
        raise NotImplementedError()

    def set_keyboard(self, keyboard: Keyboard, **kwargs):
        raise NotImplementedError()

    def get_current_user(self):
        raise NotImplementedError()

    def run(self) -> NoReturn:
        raise NotImplementedError()
