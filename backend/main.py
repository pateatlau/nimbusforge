from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

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


class ItemIn(BaseModel):
    name: str
    description: str | None = None


class Item(ItemIn):
    id: int


# Simple in-memory store (resets on server restart).
items: dict[int, Item] = {}
next_id = 1


@app.get("/items", response_model=list[Item])
async def list_items():
    return list(items.values())


@app.post("/items", response_model=Item, status_code=201)
async def create_item(payload: ItemIn):
    global next_id
    item = Item(id=next_id, **payload.model_dump())
    items[item.id] = item
    next_id += 1
    return item


@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    item = items.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, payload: ItemIn):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    item = Item(id=item_id, **payload.model_dump())
    items[item_id] = item
    return item


@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
