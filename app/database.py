from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.settings import Settings

settings = Settings()

engine = create_async_engine(settings.DATABASE_URL)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
