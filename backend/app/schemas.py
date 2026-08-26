from pydantic import BaseModel, ConfigDict, field_validator


class ItemIn(BaseModel):
    name: str
    description: str | None = None

    @field_validator("name")
    @classmethod
    def validate_nonblank_name(cls, name: str) -> str:
        if not name.strip():
            raise ValueError("name must not be blank")
        return name


class Item(ItemIn):
    id: int

    model_config = ConfigDict(from_attributes=True)