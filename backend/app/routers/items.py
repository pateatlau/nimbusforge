from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import repositories
from app.database import get_session
from app.schemas import Item, ItemIn

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[Item])
async def list_items(session: AsyncSession = Depends(get_session)):
    return await repositories.list_items(session)


@router.post("", response_model=Item, status_code=201)
async def create_item(payload: ItemIn, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        return await repositories.create_item(session, payload)


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    item = await repositories.get_item(session, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=Item)
async def update_item(
    item_id: int,
    payload: ItemIn,
    session: AsyncSession = Depends(get_session),
):
    async with session.begin():
        item = await repositories.get_item(session, item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return await repositories.update_item(session, item, payload)


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        item = await repositories.get_item(session, item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        await repositories.delete_item(session, item)