from database.db import async_session
from database.models import ResponsesModel


async def create_response(text: str):
    async with async_session() as session:
        async with session.begin():
            response = ResponsesModel(text=text)
            session.add(response)
        await session.refresh(response)

        return response