import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# モデルのインポートパスを追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import metadata
from app.database import Engine
from app.core.config import get_env

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = metadata

# その他の設定
# URLエンコーディングを使用してデータベースURLを設定
from urllib.parse import quote_plus
database_url = get_env().DATABASE_URL
parsed_url = database_url.split('://')
if len(parsed_url) == 2:
    scheme, rest = parsed_url
    user_pass, host_db = rest.split('@')
    user, password = user_pass.split(':')
    encoded_password = quote_plus(password)
    encoded_url = f"{scheme}://{user}:{encoded_password}@{host_db}"
    config.set_main_option('sqlalchemy.url', encoded_url)
else:
    config.set_main_option('sqlalchemy.url', database_url)

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = Engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
