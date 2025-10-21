 feat-landing-page
from __future__ import annotations
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# --- Make sure backend/ is on sys.path so imports work ---

# backend/migrations/env.py
from __future__ import annotations
import os, sys
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

# Ensure backend/ is importable
 main
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

 feat-landing-page
# --- Import your SQLAlchemy Base (declared in backend/db.py) ---
from db import Base  # db.py must define: Base = declarative_base()

# this is the Alembic Config object
config = context.config
fileConfig(config.config_file_name)

# tell Alembic about your models’ metadata
target_metadata = Base.metadata

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
# Import your SQLAlchemy Base (must exist)
from db import Base  # backend/db.py -> Base = declarative_base()

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    url = os.environ.get("DATABASE_URL") or config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )
    main
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    url = os.environ.get("DATABASE_URL")
    if url:
        configuration["sqlalchemy.url"] = url

    connectable = engine_from_config( feat-landing-page
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )


        configuration, prefix="sqlalchemy.", poolclass=pool.NullPool
    ) main
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()
