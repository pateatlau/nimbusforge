import asyncio
import json
from pathlib import Path

from pydantic import BaseModel, Field, TypeAdapter, field_validator
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert

from app.database import async_session_factory, engine
from app.models import Item

SEED_PATH = Path(__file__).parent.parent / "seeds" / "items.json"


class SeedItem(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1)
    description: str | None = None

    @field_validator("name")
    @classmethod
    def validate_nonblank_name(cls, name: str) -> str:
        if not name.strip():
            raise ValueError("name must not be blank")
        return name


async def seed_items(seed_path: Path = SEED_PATH) -> None:
    raw_items = json.loads(seed_path.read_text(encoding="utf-8"))
    items = TypeAdapter(list[SeedItem]).validate_python(raw_items)

    async with async_session_factory() as session:
        async with session.begin():
            for item in items:
                values = item.model_dump()
                statement = insert(Item).values(**values)
                await session.execute(
                    statement.on_conflict_do_update(
                        index_elements=[Item.id],
                        set_={
                            "name": statement.excluded.name,
                            "description": statement.excluded.description,
                        },
                    )
                )

            await session.execute(
                text(
                    "SELECT setval(pg_get_serial_sequence('items', 'id'), "
                    "COALESCE(MAX(id) + 1, 1), false) FROM items"
                )
            )


async def main() -> None:
    try:
        await seed_items()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())