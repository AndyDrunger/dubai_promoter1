from database.db import async_session
from database.models import ProxiesModel


async def create_proxy(addr: str, port: int, country: str, type: str = None,
                       username: str = None, password: str = None, rdns: bool = True) -> ProxiesModel:
    async with async_session() as session:
        async with session.begin():
            proxy = ProxiesModel(type=type, addr=addr, port=port,
                               country=country, username=username, password=password, rdns=rdns)
            session.add(proxy)
        await session.refresh(proxy)

        return proxy


