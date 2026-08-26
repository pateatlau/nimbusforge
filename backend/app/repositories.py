from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.schemas import ItemIn


async def list_items(session: AsyncSession) -> list[models.Item]:
    result = await session.scalars(select(models.Item).order_by(models.Item.id))
    return list(result)


async def get_item(session: AsyncSession, item_id: int) -> models.Item | None:
    return await session.get(models.Item, item_id)


async def create_item(session: AsyncSession, payload: ItemIn) -> models.Item:
    item = models.Item(**payload.model_dump())
    session.add(item)
    await session.flush()
    return item


async def update_item(
    session: AsyncSession, item: models.Item, payload: ItemIn
) -> models.Item:
    item.name = payload.name
    item.description = payload.description
    await session.flush()
    return item


async def delete_item(session: AsyncSession, item: models.Item) -> None:
    await session.delete(item)
    await session.flush()