from dotenv import load_dotenv

from db import async_engine, Base

# import models

load_dotenv()


async def init_models():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

