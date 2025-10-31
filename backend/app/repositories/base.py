"""
Base repository class for IQAutoJobs.
"""
from typing import Generic, TypeVar, Type, Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations."""
    
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db
    
    async def get(self, id: UUID) -> Optional[ModelType]:
        """Get record by ID."""
        result = await self.db.execute(select(self.model).filter(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_all(self) -> List[ModelType]:
        """Get all objects."""
        result = await self.db.execute(select(self.model))
        return result.scalars().all()

    async def get_by_field(self, field: str, value: Any) -> Optional[ModelType]:
        """Get record by field value."""
        result = await self.db.execute(
            select(self.model).filter(getattr(self.model, field) == value)
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[ModelType]:
        """Get multiple records with pagination and filtering."""
        query = select(self.model)

        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    if isinstance(value, list):
                        query = query.filter(getattr(self.model, field).in_(value))
                    else:
                        query = query.filter(getattr(self.model, field) == value)

        result = await self.db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, obj_in: Dict[str, Any]) -> ModelType:
        """Create a new record."""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: ModelType, obj_in: Dict[str, Any]) -> ModelType:
        """Update a record."""
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, id: UUID) -> Optional[ModelType]:
        """Delete a record."""
        db_obj = await self.get(id)
        if db_obj:
            await self.db.delete(db_obj)
            await self.db.commit()
        return db_obj

    async def exists(self, id: UUID) -> bool:
        """Check if record exists."""
        result = await self.db.execute(select(self.model.id).filter(self.model.id == id))
        return result.scalar_one_or_none() is not None

    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count records with optional filtering."""
        query = select(func.count()).select_from(self.model)

        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    if isinstance(value, list):
                        query = query.filter(getattr(self.model, field).in_(value))
                    else:
                        query = query.filter(getattr(self.model, field) == value)

        result = await self.db.execute(query)
        return result.scalar_one()
    
    async def search(
        self,
        search_fields: List[str],
        search_term: str,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ModelType]:
        """Search records by text fields."""
        query = select(self.model)
        
        # Add search conditions
        if search_term:
            search_conditions = []
            for field in search_fields:
                if hasattr(self.model, field):
                    search_conditions.append(
                        getattr(self.model, field).ilike(f"%{search_term}%")
                    )
            
            if search_conditions:
                query = query.filter(or_(*search_conditions))
        
        # Add additional filters
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    if isinstance(value, list):
                        query = query.filter(getattr(self.model, field).in_(value))
                    else:
                        query = query.filter(getattr(self.model, field) == value)
        
        result = await self.db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()
    
    async def get_by_ids(self, ids: List[UUID]) -> List[ModelType]:
        """Get multiple records by IDs."""
        result = await self.db.execute(select(self.model).filter(self.model.id.in_(ids)))
        return result.scalars().all()
