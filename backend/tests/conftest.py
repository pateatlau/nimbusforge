import os
from collections.abc import AsyncIterator, Iterator

import pytest
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete, text

os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://nimbusforge:nimbusforge_dev@localhost:55432/nimbusforge_test",
)

from app.database import async_session_factory  # noqa: E402
from app.models import Item  # noqa: E402
from main import app  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def migrated_database() -> Iterator[None]:
    config = Config("alembic.ini")
    command.upgrade(config, "head")
    command.downgrade(config, "base")
    command.upgrade(config, "head")
    yield


@pytest.fixture(autouse=True)
async def clean_items(migrated_database: None) -> AsyncIterator[None]:
    async with async_session_factory() as session:
        async with session.begin():
            await session.execute(delete(Item))
            await session.execute(
                text(
                    "SELECT setval(pg_get_serial_sequence('items', 'id'), 1, false)"
                )
            )
    yield


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    async with app.router.lifespan_context(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as test_client:
            yield test_client