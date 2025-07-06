import asyncio

from dotenv import load_dotenv

from classes.database import DbBase
from database.crud.chats import get_chats
from database.models import ChatsModel


async def main() -> None:
    load_dotenv()
    await DbBase.db_connect()

    chats = await get_chats()
    for chat in chats:
        print(chat.username)






if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())