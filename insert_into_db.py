import asyncio

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from api.core.settings import settings
from api.db.models import UserModel


async def create_user(
        async_session: async_sessionmaker[AsyncSession], user_data: dict) -> None:
    async with async_session() as session:
        async with session.begin():
            session.add(UserModel(**user_data))
            await session.commit()


async def main():
    engine = create_async_engine(settings.db_url)
    a_session = async_sessionmaker(engine, expire_on_commit=False)
    # admin = {
    #     'name': 'admin',
    #     'telegram_id': 1,
    #     'password': 'password'
    # }
    # await create_user(a_session, admin)
    # with
    await engine.dispose()


asyncio.run(main())
