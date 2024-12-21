"""Add DATA_CHECK_ERROR status

Revision ID: 338650246976
Revises: 100a8dde0c78
Create Date: 2024-12-21 02:07:14.239015

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '338650246976'
down_revision: Union[str, None] = '100a8dde0c78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = 'area_imports'
column_name = 'result_status'
enum_type_name = 'resultstatus'
enum_value = 'DATA_CHECK_ERROR'


def upgrade() -> None:
    op.execute(f"ALTER TYPE {enum_type_name} ADD VALUE '{enum_value}'")


def downgrade() -> None:
    op.execute(
        f'UPDATE {table_name}'
        f" SET {column_name} = 'SUCCESS'"
        f" WHERE {column_name} = '{enum_value}'"
    )

    enum_type_name_old = enum_type_name + '_old'
    op.execute(f'ALTER TYPE {enum_type_name} RENAME to {enum_type_name_old}')
    op.execute(
        f'CREATE TYPE {enum_type_name} AS ENUM('
        "'SUCCESS', 'DOWNLOADING_ERROR', 'PARSING_ERROR', 'EMPTY_DATA_ERROR')"
    )
    op.execute(
        f'ALTER TABLE {table_name}'
        f' ALTER COLUMN {column_name}'
        f' TYPE {enum_type_name}'
        f' USING {column_name}::text::{enum_type_name}'
    )
    op.execute(f'DROP TYPE {enum_type_name_old}')
