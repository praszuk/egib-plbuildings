"""Add building model

Revision ID: 3f695856ad1a
Revises:
Create Date: 2024-09-29 01:33:13.991277

"""

from collections.abc import Sequence

import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '3f695856ad1a'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'buildings',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column(
            'geometry',
            geoalchemy2.types.Geometry(
                srid=4326, from_text='ST_GeomFromEWKT', name='geometry', nullable=False
            ),
            nullable=False,
        ),
        sa.Column('tags', sa.JSON(), nullable=False),
        sa.Column('teryt', sa.String(length=8), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('buildings')
