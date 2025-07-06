import asyncio

import socks
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

from classes.database import DbReader, DbBase
from main_app.db_new.main import add_acc
from main_app.telethon.main import get_connected_client


ids = [
6607220179,7347946933,6626852373,7559824749
]


async def main(acc_ids: list[int]):
    load_dotenv()
    await DbBase.db_connect()

    proxy_id = 2

    for acc_id in acc_ids:
        string_session = await get_string_session_from_session_file(acc_id, proxy_id=proxy_id)
        await add_acc(acc_id=acc_id, string_session=string_session, api_id=2040,
                      api_hash='b18441a1ff607e10a989891a5462e627', proxy_id=proxy_id)



async def get_string_session_from_session_file(acc_id, proxy_id):
    client = await get_client(acc_id, proxy_id=proxy_id)
    string_session = StringSession.save(client.session)
    print(string_session)
    return string_session


async def get_client(acc_id: int, proxy_id: int) -> TelegramClient:
    session_file_path = f'sessions/{acc_id}.session'
    proxy = await DbReader.get_proxy(proxy_id=proxy_id)

    client = TelegramClient(
        session=session_file_path,
        api_id=2040,
        api_hash='b18441a1ff607e10a989891a5462e627',
        proxy=proxy,
    )

    return client


if __name__ == '__main__':
    asyncio.run(main(ids))
