"""
Абстракция сообщения бота.
"""

from dataclasses import dataclass


@dataclass
class Message:
    text: str
