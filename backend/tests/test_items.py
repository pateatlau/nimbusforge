from unittest.mock import AsyncMock

from httpx import ASGITransport, AsyncClient
from pytest import MonkeyPatch
from sqlalchemy.exc import OperationalError

import main
from app.database import get_session


async def test_item_crud_contract(client: AsyncClient) -> None:
    assert (await client.get("/items")).json() == []

    created_response = await client.post(
        "/items",
        json={"name": "Persisted item", "description": None},
    )
    assert created_response.status_code == 201
    created = created_response.json()
    assert created == {"id": 1, "name": "Persisted item", "description": None}

    assert (await client.get("/items/1")).json() == created

    updated_response = await client.put(
        "/items/1",
        json={"name": "Updated item", "description": "Stored in PostgreSQL"},
    )
    assert updated_response.status_code == 200
    assert updated_response.json() == {
        "id": 1,
        "name": "Updated item",
        "description": "Stored in PostgreSQL",
    }

    deleted_response = await client.delete("/items/1")
    assert deleted_response.status_code == 204
    assert deleted_response.content == b""


async def test_item_not_found_contract(client: AsyncClient) -> None:
    expected = {"detail": "Item not found"}
    assert (await client.get("/items/999")).json() == expected
    assert (
        await client.put(
            "/items/999",
            json={"name": "Missing", "description": None},
        )
    ).json() == expected
    assert (await client.delete("/items/999")).json() == expected


async def test_startup_fails_when_database_is_unavailable(
    monkeypatch: MonkeyPatch,
) -> None:
    unavailable = OperationalError("SELECT 1", {}, Exception("unavailable"))
    monkeypatch.setattr(
        main,
        "check_database_connection",
        AsyncMock(side_effect=unavailable),
    )

    try:
        async with main.app.router.lifespan_context(main.app):
            pass
    except OperationalError as error:
        assert error is unavailable
    else:
        raise AssertionError("Startup unexpectedly succeeded")


async def test_request_returns_503_after_database_outage() -> None:
    class UnavailableSession:
        async def scalars(self, _):
            raise OperationalError("SELECT items", {}, Exception("unavailable"))

    async def unavailable_session():
        yield UnavailableSession()

    main.app.dependency_overrides[get_session] = unavailable_session
    try:
        async with AsyncClient(
            transport=ASGITransport(app=main.app, raise_app_exceptions=False),
            base_url="http://test",
        ) as client:
            response = await client.get("/items")
    finally:
        main.app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}