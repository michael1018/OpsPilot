"""
Async database access layer for OpsPilot
----------------------------------------
Provides common CRUD operations based on SQLAlchemy async ORM.
"""

import uuid
from typing import Union, List, Optional, Iterable

from core.api.api_response import ApiResponse
from core.api.api_context import ApiContext
from core.exceptions import ApiException, ApiError
from core.utils.assertion import Assert

from database.orm import ModelBase
from database.aio_session import scope_session

__all__ = [
    'add',
    'find',
    'fetch',
    'fetch_pages',
    'update',
    'delete',
    'restore',
]


# ------------------------------
# Helper
# ------------------------------
def ensure_list(value: Union[str, Iterable]) -> List:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return [value]


# ------------------------------
# CRUD Operations
# ------------------------------
async def add(table: ModelBase, model: dict, context: Optional[ApiContext] = None, conflict_nothing: Optional[str] = None):
    Assert.is_not_dict(model, 'model cannot be empty')
    model.setdefault('id', uuid.uuid4().hex)
    return await scope_session.add(table, conflict_nothing=conflict_nothing, **model)


async def find(table: ModelBase, id: str, has_deleted: bool = False):
    Assert.is_not_null(id, 'id cannot be null')
    query = scope_session.select(table).where(table.id == id)
    if hasattr(table, 'is_deleted'):
        query = query.where(table.is_deleted == has_deleted)
    return await query.fetchrow()


async def fetch(table: ModelBase, columns: List, criterions: Optional[List] = None):
    Assert.is_not_list(columns, 'columns', True)
    Assert.is_not_list(criterions, 'criterions', True)
    query = scope_session.select(*columns)
    if hasattr(table, 'is_deleted'):
        query = query.where(table.is_deleted == False)
    return await query.where_criterions(table, criterions).fetch()


async def update(table: ModelBase, model: dict):
    Assert.is_not_dict(model, 'model cannot be empty')
    record_id = model.pop('id', None)
    if not record_id:
        raise ApiError(f'Update failed: id is required for {table.__tablename__}')
    return await scope_session.update(table).where(table.id == record_id).values(**model).execute()


async def delete(table: ModelBase, id: Union[str, List[str]], delete_reason: str = None, permanent: bool = False):
    Assert.is_not_null(id, 'id cannot be null')
    ids = ensure_list(id)
    if hasattr(table, 'is_deleted') and not permanent:
        return await scope_session.update(table).where(table.id.in_(ids)).values(is_deleted=True, delete_reason=delete_reason).execute()
    return await scope_session.delete(table).where(table.id.in_(ids)).execute()


async def restore(table: ModelBase, ids: Union[str, List[str]], **values):
    Assert.is_not_null(ids, 'ids cannot be null')
    if not hasattr(table, 'is_deleted'):
        raise ApiException(400, 'This table does not support restore operation')
    id_list = ensure_list(ids)
    return await scope_session.update(table).where(table.id.in_(id_list)).values(is_deleted=False, delete_reason=None, **values).execute()


async def fetch_pages(table: ModelBase, pageindex: int = 0, pagesize: int = 10, criterions: Optional[List] = None,
                      sortby: Optional[str] = None, descending: bool = False, deleted: bool = False):
    Assert.is_not_null(table, 'table cannot be null')
    Assert.is_not_int(pageindex, 'pageindex')
    Assert.is_not_int(pagesize, 'pagesize')
    Assert.is_not_list(criterions, 'criterions', nullable=True)
    Assert.is_not_bool(deleted, 'deleted')

    pageindex = max(pageindex, 0)
    pagesize = max(pagesize, 1)

    query = scope_session.select(table).where_criterions(table, criterions)
    if hasattr(table, 'is_deleted'):
        query = query.where(table.is_deleted == deleted)

    data, total = await query.order_by_with(table, sortby, descending).limit(pagesize).offset(pageindex * pagesize).fetchpages()
    return ApiResponse.success(data=data, total=total)
