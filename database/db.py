import os

from dotenv import load_dotenv

load_dotenv()

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# не импортируйте models и init_db здесь

async_engine = create_async_engine(
    os.getenv("POSTGRES_AWS_URL"),
    echo=False
)

async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    pass

