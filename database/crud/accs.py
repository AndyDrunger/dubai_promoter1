from database.db import async_session
from database.models import AccsModel


async def create_acc(id: int, api_id: int, api_hash: str, proxy_id: int, profile_id: int,
                     string_session: str, status: str = None) -> AccsModel:
    async with async_session() as session:
        async with session.begin():
            acc = AccsModel(id=id, api_id=api_id, api_hash=api_hash, proxy_id=proxy_id,
                            profile_id=profile_id, string_session=string_session, status=status)
            session.add(acc)
        await session.refresh(acc)
        return acc
