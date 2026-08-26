from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from app import repositories
from app.database import check_database_connection, engine, get_session
from app.schemas import Item, ItemIn


@asynccontextmanager
async def lifespan(_: FastAPI):
    await check_database_connection()
    try:
        yield
    finally:
        await engine.dispose()


app = FastAPI(lifespan=lifespan)

# Allow the Vite dev server (and any local origin) to call the API directly.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(OperationalError)
async def database_unavailable(_: Request, __: OperationalError) -> JSONResponse:
    return JSONResponse(status_code=503, content={"detail": "Database unavailable"})


@app.get("/items", response_model=list[Item])
async def list_items(session: AsyncSession = Depends(get_session)):
    return await repositories.list_items(session)


@app.post("/items", response_model=Item, status_code=201)
async def create_item(payload: ItemIn, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        return await repositories.create_item(session, payload)


@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    item = await repositories.get_item(session, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=Item)
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


@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        item = await repositories.get_item(session, item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        await repositories.delete_item(session, item)
