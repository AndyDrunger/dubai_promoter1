from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Chat:
    id: int
    sg_id: int = field(init=False)
    username: Optional[str] = None
    inv_link: Optional[str] = None
    input_channel: Optional[object] = None
    captcha: bool = field(default=False)

    def __post_init__(self):
        self.sg_id = int(f'-100{self.id}')