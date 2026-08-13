"""add location slug

Revision ID: 0313f439dc9d
Revises: 5ad24097d703
Create Date: 2026-08-13 23:00:09.122697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '0313f439dc9d'
down_revision: Union[str, Sequence[str], None] = '5ad24097d703'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("location", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("slug", sqlmodel.sql.sqltypes.AutoString(), nullable=True)
        )

    op.execute("UPDATE location SET slug = 'rzeszow' WHERE name = 'Rzeszów'")
    op.execute("UPDATE location SET slug = 'zakopane' WHERE name = 'Zakopane'")
    op.execute("UPDATE location SET slug = 'sopot' WHERE name = 'Sopot'")
    op.execute(
        "UPDATE location SET slug = 'suwalki', name = 'Suwałki' "
        "WHERE name IN ('Suwalki', 'Suwałki')"
    )

    with op.batch_alter_table("location", schema=None) as batch_op:
        batch_op.alter_column(
            "slug",
            existing_type=sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
        )
        batch_op.create_unique_constraint("uq_location_slug", ["slug"])


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("location", schema=None) as batch_op:
        batch_op.drop_constraint("uq_location_slug", type_="unique")
        batch_op.drop_column("slug")
