"""Add building model

Revision ID: 3f695856ad1a
Revises:
Create Date: 2024-09-29 01:33:13.991277

"""

from typing import Sequence, Union

import geoalchemy2
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f695856ad1a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


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
