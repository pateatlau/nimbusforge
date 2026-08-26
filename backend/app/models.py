from sqlalchemy import BigInteger, CheckConstraint, Identity, Index, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Item(Base):
    __tablename__ = "items"
    __table_args__ = (
        CheckConstraint("length(btrim(name)) > 0", name="ck_items_name_nonblank"),
        Index("ix_items_name", "name"),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)