from typing import Any, Coroutine

from sqlalchemy import select

from classes.chat import Chat
from database.db import async_session
from database.mapper import map_model_to_business
from database.models import ChatsModel


async def create_chat(id: int, captcha: bool = False, username: str = None, inv_link: str = None):
    async with async_session() as session:
        async with session.begin():
            chat = ChatsModel(id=id, captcha=captcha, username=username, inv_link=inv_link)
            session.add(chat)
        await session.refresh(chat)

        return chat


async def get_chats() -> list[Chat]:
    async with async_session() as session:
        query = select(ChatsModel)
        result = await session.execute(query)
        chat_models = result.unique().scalars().all()

        return [map_model_to_business(chat, Chat) for chat in chat_models]


async def get_chat(id: int) -> Chat:
    async with async_session() as session:
        query = select(ChatsModel).where(ChatsModel.id == id)
        result = await session.execute(query)
        chat_model = result.unique().scalars().one()

        return map_model_to_business(chat_model, Chat)