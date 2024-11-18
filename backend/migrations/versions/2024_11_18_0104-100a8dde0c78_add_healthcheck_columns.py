"""Add healthcheck columns

Revision ID: 100a8dde0c78
Revises: 2aa2de043ff7
Create Date: 2024-11-18 01:04:30.603855

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '100a8dde0c78'
down_revision: Union[str, None] = '2aa2de043ff7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('area_imports', sa.Column('hc_lat', sa.Float(), nullable=True))
    op.add_column('area_imports', sa.Column('hc_lon', sa.Float(), nullable=True))
    op.add_column('area_imports', sa.Column('hc_expected_tags', sa.JSON(), nullable=True))
    op.add_column('area_imports', sa.Column('hc_result_tags', sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column('area_imports', 'hc_result_tags')
    op.drop_column('area_imports', 'hc_expected_tags')
    op.drop_column('area_imports', 'hc_lon')
    op.drop_column('area_imports', 'hc_lat')
