"""Create items table.

Revision ID: 0001
Revises:
"""

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.create_table(
        "items",
        sa.Column(
            "id",
            sa.BigInteger(),
            sa.Identity(always=False),
            nullable=False,
        ),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.CheckConstraint(
            "length(btrim(name)) > 0",
            name="ck_items_name_nonblank",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_items_name", "items", ["name"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_items_name", table_name="items")
    op.drop_table("items")