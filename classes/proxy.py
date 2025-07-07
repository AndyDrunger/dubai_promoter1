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

    rdns: Union[int, bool]




    def __post_init__(self):
        if self.type == 'socks5':
            self.type = socks.PROXY_TYPE_SOCKS5

        if self.rdns == 1:
            self.rdns = True


    def to_tuple(self) -> tuple:
        return (self.addr, self.port, True, self.username, self.password)


    def to_dict(self) -> dict:
        return {
            'proxy_type': self.type,
            'addr': self.addr,
            'port': self.port,
            'username': self.username,
            'password': self.password,
            'rdns': self.rdns,
        }