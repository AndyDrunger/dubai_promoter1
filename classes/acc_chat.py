import enum
from dataclasses import dataclass

from classes.chat import Chat


class AccChatStatus(enum.Enum):
    unjoined = 'unjoined'
    joined = 'joined'
    banned = 'banned'
    requested = 'requested'
    muted = 'muted'
    kicked = 'kicked'
    problem = 'problem'


@dataclass
class AccChat(Chat):
    status: AccChatStatus = None
    """
    Представляет чат в контексте аккаунта.
    Наследует поля чата, добавляя статус связи.
    """
