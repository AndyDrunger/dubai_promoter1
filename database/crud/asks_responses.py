from sqlalchemy import select

from classes.promo_script import PromoScript
from database.db import async_session
from database.mapper import map_asks_responses_to_promo_script
from database.models import AsksResponsesModel


async def create_ask_response(ask_id: int, response_id: int) -> AsksResponsesModel:
    async with async_session() as session:
        async with session.begin():
            ask_response = AsksResponsesModel(ask_id=ask_id, response_id=response_id)
            session.add(ask_response)
        await session.refresh(ask_response)

        return ask_response


async def get_promo_scripts() -> list[PromoScript]:
    async with async_session() as session:
        query = select(AsksResponsesModel)
        result = await session.execute(query)
        asks_responses_models = result.unique().scalars().all()

        return [map_asks_responses_to_promo_script(ar) for ar in asks_responses_models]


async def get_promo_script(id: int) -> PromoScript:
    async with async_session() as session:
        query = select(AsksResponsesModel).where(AsksResponsesModel.id == id)
        result = await session.execute(query)
        asks_responses_model = result.scalars().one()

        return map_asks_responses_to_promo_script(asks_responses_model)