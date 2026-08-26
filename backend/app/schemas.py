from pydantic import BaseModel, ConfigDict


class ItemIn(BaseModel):
    name: str
    description: str | None = None


class Item(ItemIn):
    id: int

    model_config = ConfigDict(from_attributes=True)