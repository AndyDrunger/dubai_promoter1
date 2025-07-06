from sqlalchemy import select, update

from classes.acc import Acc, AccStatus
from database.db import async_session
from database.mapper import map_model_to_business, map_acc_model_to_business
from database.models import AccsModel


async def create_acc(id: int, api_id: int, api_hash: str, proxy_id: int, profile_id: int,
                     string_session: str, status: str = None) -> AccsModel:
    async with async_session() as session:
        async with session.begin():
            acc = AccsModel(id=id, api_id=api_id, api_hash=api_hash, proxy_id=proxy_id,
                            profile_id=profile_id, string_session=string_session, status=status)
            session.add(acc)
        await session.refresh(acc)

        return acc


async def get_accs() -> list[Acc]:
    async with async_session() as session:
        query = select(AccsModel)
        result = await session.execute(query)
        acc_models = result.unique().scalars().all()

        return [map_acc_model_to_business(acc) for acc in acc_models]


async def get_acc(id: int) -> Acc:
    async with async_session() as session:
        query = select(AccsModel).where(AccsModel.id == id)
        result = await session.execute(query)
        acc_model = result.scalars().first()

        return map_acc_model_to_business(acc_model)


async def update_acc_status(acc_id: int, status: AccStatus) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(AccsModel)
                .where(AccsModel.id == acc_id)
                .values(status=status.value)
            )