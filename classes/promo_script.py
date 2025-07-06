from dataclasses import dataclass
from typing import Optional


@dataclass
class Ask:
    id: int
    text: str

@dataclass
class Response:
    id: int
    text: str


@dataclass
class PromoScript:
    id: int
    ask: Ask
    response: Response
    ask_msg_id: Optional[int] = None
    ask_acc_id: Optional[int] = None
    response_msg_id: Optional[int] = None
    response_acc_id: Optional[int] = None

