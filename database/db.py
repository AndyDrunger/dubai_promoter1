import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

async_engine = create_async_engine(
    os.getenv("POSTGRES_LOCAL_URL"),
    echo=True
)


async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    pass


