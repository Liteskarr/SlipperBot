"""
Абстракция кнопки бота.
"""

from dataclasses import dataclass
from enum import Enum


class ButtonColor(Enum):
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    NEGATIVE = 'negative'
    POSITIVE = 'positive'


@dataclass
class Button:
    text: str
    color: ButtonColor
