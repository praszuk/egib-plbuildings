from logging.config import fileConfig
from typing import Optional, Literal

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from sqlalchemy.sql.schema import SchemaItem

from backend.core.config import settings
from backend.database.base import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

IGNORE_TABLES: list[str] = ['spatial_ref_sys']


def include_object(
    object: SchemaItem,  # noqa
    name: Optional[str],
    type_: Literal[
        'schema',
        'table',
        'column',
        'index',
        'unique_constraint',
        'foreign_key_constraint',
    ],
    reflected: bool,  # noqa
    compare_to: Optional[SchemaItem],  # noqa
) -> bool:
    if type_ == 'table' and (name in IGNORE_TABLES or object.info.get('skip_autogenerate', False)):
        return False

    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section, {})
    configuration['sqlalchemy.url'] = settings.DATABASE_URL
    connectable = engine_from_config(
        configuration,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, include_object=include_object
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
