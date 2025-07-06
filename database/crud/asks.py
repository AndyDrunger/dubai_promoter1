from database.db import async_session
from database.models import AsksModel


async def create_ask(text: str):
    async with async_session() as session:
        async with session.begin():
            ask = AsksModel(text=text)
            session.add(ask)
        await session.refresh(ask)

        return ask