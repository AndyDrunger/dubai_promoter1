import asyncio

from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import inspect

from database.crud.chats import get_chats
from database.db import async_engine, Base
from database.models import ChatsModel



async def check_db_tables():
    async with async_engine.connect() as conn:
        def sync_get_tables(sync_conn):
            inspector = inspect(sync_conn)
            return inspector.get_table_names()

        tables_in_db = await conn.run_sync(sync_get_tables)
        print("Таблицы в БД:", tables_in_db)

    # Сравнить с моделями
    models_tables = Base.metadata.tables.keys()
    print("Таблицы в моделях:", list(models_tables))

    missing = set(models_tables) - set(tables_in_db)
    if missing:
        print("В базе отсутствуют таблицы:", missing)
    else:
        print("Все таблицы моделей присутствуют в базе.")


async def main() -> None:
    await check_db_tables()


if __name__ == "__main__":
    asyncio.run(main())