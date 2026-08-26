import json
from pathlib import Path

import pytest
from pydantic import ValidationError
from sqlalchemy import inspect, select
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine import make_url

from app import repositories
from app.config import get_settings
from app.database import async_session_factory, check_database_connection, engine
from app.models import Item
from app.schemas import ItemIn
from app.seed import SEED_PATH, seed_items


async def test_migration_creates_expected_schema() -> None:
    async with engine.connect() as connection:
        tables = await connection.run_sync(lambda sync: inspect(sync).get_table_names())
        indexes = await connection.run_sync(
            lambda sync: inspect(sync).get_indexes("items")
        )
        checks = await connection.run_sync(
            lambda sync: inspect(sync).get_check_constraints("items")
        )

    assert "items" in tables
    assert {index["name"] for index in indexes} == {"ix_items_name"}
    assert {check["name"] for check in checks} == {"ck_items_name_nonblank"}


async def test_multiple_operations_commit_together() -> None:
    async with async_session_factory() as session:
        async with session.begin():
            await repositories.create_item(session, ItemIn(name="First"))
            await repositories.create_item(session, ItemIn(name="Second"))

    async with async_session_factory() as session:
        names = list(await session.scalars(select(Item.name).order_by(Item.id)))

    assert names == ["First", "Second"]


async def test_constraint_failure_rolls_back_entire_transaction() -> None:
    with pytest.raises(IntegrityError):
        async with async_session_factory() as session:
            async with session.begin():
                await repositories.create_item(session, ItemIn(name="Valid"))
                await repositories.create_item(session, ItemIn(name="   "))

    async with async_session_factory() as session:
        assert list(await session.scalars(select(Item))) == []


async def test_seed_is_idempotent_and_aligns_identity() -> None:
    expected_count = len(json.loads(SEED_PATH.read_text(encoding="utf-8")))
    await seed_items()
    await seed_items()

    async with async_session_factory() as session:
        items = list(await session.scalars(select(Item).order_by(Item.id)))

    async with async_session_factory() as session:
        async with session.begin():
            created = await repositories.create_item(session, ItemIn(name="After seed"))

    assert len(items) == expected_count
    assert created.id == 4


async def test_invalid_seed_rolls_back_without_partial_writes(tmp_path: Path) -> None:
    invalid_seed = tmp_path / "items.json"
    invalid_seed.write_text(
        json.dumps(
            [
                {"id": 10, "name": "Would be valid", "description": None},
                {"id": 11, "name": "   ", "description": None},
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValidationError):
        await seed_items(invalid_seed)

    async with async_session_factory() as session:
        assert list(await session.scalars(select(Item))) == []


async def test_unavailable_database_connection_fails() -> None:
    unavailable_url = make_url(get_settings().database_url).set(port=65432)
    unavailable_engine = create_async_engine(unavailable_url)
    try:
        with pytest.raises((OSError, OperationalError)):
            await check_database_connection(unavailable_engine)
    finally:
        await unavailable_engine.dispose()