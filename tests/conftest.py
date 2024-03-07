from typing import AsyncGenerator

from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from src.config import settings
from src.database.db import get_async_session
from src.main import app
from src.statistic.models import Statistic, Base


test_async_engine = create_async_engine(
    url=settings.TEST_DATABASE_URL_asyncpg,
    poolclass=NullPool,
)

test_async_session_factory = async_sessionmaker(test_async_engine)
Base.metadata.bind = test_async_engine


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session_factory() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(scope='function')
async def async_client() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as async_client:
        yield async_client


@pytest.fixture(autouse=True, scope='function')
async def prepare_database():
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
