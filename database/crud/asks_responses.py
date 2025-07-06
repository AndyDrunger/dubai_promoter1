from database.db import async_session
from database.models import AsksResponsesModel


async def create_ask_response(ask_id: int, response_id: int) -> AsksResponsesModel:
    async with async_session() as session:
        async with session.begin():
            ask_response = AsksResponsesModel(ask_id=ask_id, response_id=response_id)
            session.add(ask_response)
        await session.refresh(ask_response)
        return ask_response