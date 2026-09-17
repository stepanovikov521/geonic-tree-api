import logging
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Import the Base class and metadata
from models.class_Base import Base

# Explicitly import models to register them with the metadata for autogenerate support.
# Using explicit imports instead of '*' is a best practice to avoid namespace pollution.
from models.models_relative import Relative
from models.models_user import User

# Alembic configuration
config = context.config
target_metadata = Base.metadata

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

logger = logging.getLogger(__name__)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
    except Exception as e:
        logger.error(f"Error during offline migrations: {e}", exc_info=True)
        sys.exit(1)


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    try:
        with connectable.connect() as connection:
            context.configure(connection=connection, target_metadata=target_metadata)
            with context.begin_transaction():
                context.run_migrations()
    except Exception as e:
        logger.error(f"Error during online migrations: {e}", exc_info=True)
        sys.exit(1)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
