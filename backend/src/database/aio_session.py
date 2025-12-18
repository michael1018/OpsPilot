# core/database/async_session.py
"""
Async SQLAlchemy session scope for OpsPilot
-------------------------------------------
Provides async session context for CRUD operations.
"""

from typing import Any, List, Optional, Tuple
import sqlalchemy as sa
import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from contextlib import asynccontextmanager

from core.exceptions import ApiError
from dotenv import load_dotenv

# ------------------------------
# Engine & Session Factory
# ------------------------------
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in environment")

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
AsyncSessionFactory = async_sessionmaker(bind=engine, expire_on_commit=False)


# ------------------------------
# Async session context manager
# ------------------------------
@asynccontextmanager
async def get_async_session():
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ------------------------------
# Query Builder
# ------------------------------
class Query:
    def __init__(self, session: AsyncSession, stmt: sa.sql.Select):
        self.session = session
        self.stmt = stmt

    def where(self, condition: Any):
        self.stmt = self.stmt.where(condition)
        return self

    def where_criterions(self, criterions: Optional[List[Any]]):
        if criterions:
            for c in criterions:
                self.stmt = self.stmt.where(c)
        return self

    def order_by_with(self, table, sortby: Optional[str], descending: bool = False):
        if sortby:
            column = getattr(table, sortby, None)
            if not column:
                raise ApiError(f"Invalid sort column: {sortby}")
            self.stmt = self.stmt.order_by(column.desc() if descending else column.asc())
        return self

    def limit(self, value: int):
        self.stmt = self.stmt.limit(value)
        return self

    def offset(self, value: int):
        self.stmt = self.stmt.offset(value)
        return self

    async def fetch(self) -> List[Any]:
        result = await self.session.execute(self.stmt)
        return result.scalars().all()

    async def fetchrow(self) -> Any:
        result = await self.session.execute(self.stmt)
        return result.scalars().first()

    async def fetchpages(self) -> Tuple[List[Any], int]:
        count_stmt = sa.select(sa.func.count()).select_from(self.stmt.subquery())
        total = await self.session.scalar(count_stmt)
        result = await self.session.execute(self.stmt)
        return result.scalars().all(), total


# ------------------------------
# Write Operations
# ------------------------------
class WriteQuery:
    def __init__(self, session: AsyncSession, stmt):
        self.session = session
        self.stmt = stmt

    def where(self, condition: Any):
        self.stmt = self.stmt.where(condition)
        return self

    def values(self, **values):
        self.stmt = self.stmt.values(**values)
        return self

    async def execute(self):
        await self.session.execute(self.stmt)
        await self.session.commit()
        return True
