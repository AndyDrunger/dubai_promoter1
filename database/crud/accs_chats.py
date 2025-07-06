from database.db import async_session
from database.models import AccsChatsModel


async def create_acc_chat(acc_id: int, chat_id: int, status: str = None) -> AccsChatsModel:
    async with async_session() as session:
        async with session.begin():
            acc_chat = AccsChatsModel(acc_id=acc_id, chat_id=chat_id, status=status)
            session.add(acc_chat)
        await session.refresh(acc_chat)
        return acc_chat