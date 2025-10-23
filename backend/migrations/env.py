from __future__ import annotations
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# --- Make sure backend/ is on sys.path so imports work ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# --- Import your SQLAlchemy Base and models ---
from backend.extensions import db
from backend.models import User, Job, Application, UserProfile, CompanyProfile

# Use Flask-SQLAlchemy's Model.metadata
target_metadata = db.Model.metadata

# this is the Alembic Config object
config = context.config
fileConfig(config.config_file_name)

def run_migrations_offline():
    url = os.environ.get("DATABASE_URL")
    if url:
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            compare_type=True,
        )
    else:
        context.configure(
            url=config.get_main_option("sqlalchemy.url"),
            target_metadata=target_metadata,
            literal_binds=True,
            compare_type=True,
        )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    url = os.environ.get("DATABASE_URL")
    if url:
        configuration["sqlalchemy.url"] = url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()
