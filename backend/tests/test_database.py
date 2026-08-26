import asyncio
import json
from pathlib import Path

import pytest
from httpx import AsyncClient
from pydantic import ValidationError
from sqlalchemy import inspect, select, text
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
                session.add(Item(name="   "))
                await session.flush()

    async with async_session_factory() as session:
        assert list(await session.scalars(select(Item))) == []


async def test_seed_is_idempotent_and_aligns_identity() -> None:
    seed_rows = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    expected_next_id = max((row["id"] for row in seed_rows), default=0) + 1
    await seed_items()
    await seed_items()

    async with async_session_factory() as session:
        items = list(await session.scalars(select(Item).order_by(Item.id)))

    async with async_session_factory() as session:
        async with session.begin():
            created = await repositories.create_item(session, ItemIn(name="After seed"))

    assert len(items) == len(seed_rows)
    assert created.id == expected_next_id


async def test_seed_serializes_with_api_creation(client: AsyncClient) -> None:
    seed_rows = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    expected_next_id = max((row["id"] for row in seed_rows), default=0) + 1

    async def wait_for_lock(mode: str) -> None:
        for _ in range(100):
            async with async_session_factory() as observer:
                waiting = await observer.scalar(
                    text(
                        "SELECT EXISTS ("
                        "SELECT 1 FROM pg_locks locks "
                        "JOIN pg_class tables ON tables.oid = locks.relation "
                        "WHERE tables.relname = 'items' "
                        "AND locks.mode = :mode AND NOT locks.granted)"
                    ),
                    {"mode": mode},
                )
            if waiting:
                return
            await asyncio.sleep(0.01)
        raise AssertionError(f"Timed out waiting for {mode}")

    async with async_session_factory() as blocker:
        async with blocker.begin():
            await blocker.execute(text("LOCK TABLE items IN ACCESS EXCLUSIVE MODE"))

            seed_task = asyncio.create_task(seed_items())
            await wait_for_lock("ShareRowExclusiveLock")

            create_task = asyncio.create_task(
                client.post(
                    "/items",
                    json={"name": "Created concurrently", "description": None},
                )
            )
            await wait_for_lock("RowExclusiveLock")

    await seed_task
    response = await create_task

    assert response.status_code == 201
    assert response.json()["id"] == expected_next_id


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