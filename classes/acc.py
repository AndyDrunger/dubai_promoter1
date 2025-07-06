import enum
from dataclasses import dataclass, field
from typing import Optional

from telethon.sessions import StringSession

from classes.acc_chat import AccChat
from classes.proxy import Proxy


class AccStatus(enum.Enum):
    free = "free"
    working = "working"
    problem = "problem"
    blocked = "blocked"


@dataclass
class Acc:
    id: int
    api_id: int
    api_hash: str
    status: AccStatus
    proxy_id: int
    profile_id: int
    string_session: StringSession

    # profile: Optional[Profile] = None
    chats: list[AccChat] = field(default_factory=list)
    proxy: Optional[Proxy] = None

