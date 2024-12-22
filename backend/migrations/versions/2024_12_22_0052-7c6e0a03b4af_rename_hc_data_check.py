"""Rename hc->data_check

Revision ID: 7c6e0a03b4af
Revises: 338650246976
Create Date: 2024-12-22 00:52:38.491919

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '7c6e0a03b4af'
down_revision: Union[str, None] = '338650246976'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('area_imports', schema=None) as batch_op:
        batch_op.alter_column('hc_lat', new_column_name='data_check_lat')
        batch_op.alter_column('hc_lon', new_column_name='data_check_lon')
        batch_op.alter_column('hc_result_tags', new_column_name='data_check_result_tags')
        batch_op.alter_column('hc_expected_tags', new_column_name='data_check_expected_tags')


def downgrade() -> None:
    with op.batch_alter_table('area_imports', schema=None) as batch_op:
        batch_op.alter_column('data_check_lat', new_column_name='hc_lat')
        batch_op.alter_column('data_check_lon', new_column_name='hc_lon')
        batch_op.alter_column('data_check_result_tags', new_column_name='hc_result_tags')
        batch_op.alter_column('data_check_expected_tags', new_column_name='hc_expected_tags')
