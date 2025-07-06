from sqlalchemy import select

from database.db import async_session
from database.models import ChatsModel


async def create_chat(id: int, captcha: bool = False, username: str = None, inv_link: str = None):
    async with async_session() as session:
        async with session.begin():
            chat = ChatsModel(id=id, captcha=captcha, username=username, inv_link=inv_link)
            session.add(chat)
        await session.refresh(chat)
        return chat


async def get_chats():
    async with async_session() as session:
        query = select(ChatsModel)
        result = await session.execute(query)
        chats = result.scalars().all()
        return chats