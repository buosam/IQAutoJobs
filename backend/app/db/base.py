"""
Database configuration and session management.
"""
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# Programmatically ensure the correct async driver is used
db_url = make_url(settings.DATABASE_URL)
if db_url.drivername.startswith("postgresql"):
    db_url = db_url._replace(drivername="postgresql+asyncpg")

# Create SQLAlchemy engine
engine = create_async_engine(
    db_url,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.DEBUG,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

# Create base class for models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Get database session."""
    async with SessionLocal() as db:
        yield db


async def create_tables():
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    """Drop all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
