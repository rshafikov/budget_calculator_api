from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from api.core import settings

engine = create_async_engine(settings.db_url, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
