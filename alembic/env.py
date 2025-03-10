import os
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context
from app.models import Base  # Ensure this points to your models

# Load Alembic configuration
config = context.config  # Ensure this is defined before setting options

# Set up logging if an Alembic config file exists
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Fetch the database URL from environment variables (fallback to default)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/budgetdb")

# Set the database URL in the Alembic configuration
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Add metadata for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
