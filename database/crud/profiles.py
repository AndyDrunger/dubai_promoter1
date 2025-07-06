from database.db import async_session
from database.models import ProfilesModel


async def create_profile(first_name: str, last_name: str = None, user_name: str = None,
                         about: str = None, status: str = None) -> ProfilesModel:
    async with async_session() as session:
        async with session.begin():
            profile = ProfilesModel(first_name=first_name, last_name=last_name,
                                    user_name=user_name, about=about, status=status)
            session.add(profile)
        await session.refresh(profile)

        return profile