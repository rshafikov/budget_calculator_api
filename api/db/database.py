from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession, async_sessionmaker
)

DATABASE_URL = 'postgresql://user:password@localhost/budget_bot'

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    try:
        async with async_session() as session:
            yield session
    finally:
        await session.close()
