"""
Абстракция клавиатуры.
"""

from typing import Iterable, Tuple

from abstractions.button import Button


class Keyboard:
    def __init__(self, *buttons):
        self._buttons = {}
        for pos, button in buttons:
            row, column = pos
            self.add(button, row, column)

    def add(self, button: Button, row: int, column: int):
        self._buttons[row, column] = button

    def all(self) -> Iterable[Tuple[Tuple[int, int], Button]]:
        yield from (item for item in sorted(self._buttons.items()))
