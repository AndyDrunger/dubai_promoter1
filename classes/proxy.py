from dataclasses import dataclass
from typing import Union
import socks

@dataclass
class Proxy:
    id: int
    type: Union[str, int]
    addr: str
    port: int
    username: str
    password: str


    def __post_init__(self):
        if self.type == 'socks5':
            self.type = socks.PROXY_TYPE_SOCKS5


    def to_tuple(self) -> tuple:
        return (self.addr, self.port, True, self.username, self.password)
