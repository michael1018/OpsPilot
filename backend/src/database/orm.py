"""
SQLAlchemy ORM base for OpsPilot
--------------------------------
Defines declarative base with default schema 'opspilot'.
Includes mixins for audit, remark, and soft delete.
"""

import sqlalchemy as sa
from sqlalchemy import Column, MetaData
from sqlalchemy.orm import declarative_base, declared_attr
from sqlalchemy.dialects.postgresql import UUID

# ------------------------------
# Base metadata
# ------------------------------
metadata = MetaData(schema='opspilot')
ModelBase = declarative_base(metadata=metadata)

# ------------------------------
# Mixins
# ------------------------------
class AuditMixin:
    """Mixin for audit fields"""

    @declared_attr
    def created_at(cls):
        return Column(sa.DateTime, server_default=sa.text("timezone('UTC-8'::text, now())"), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(sa.DateTime, server_default=sa.text("timezone('UTC-8'::text, now())"),
                      onupdate=sa.func.now(), nullable=False)

    @declared_attr
    def created_by_id(cls):
        return Column(UUID, nullable=True)

    @declared_attr
    def updated_by_id(cls):
        return Column(UUID, nullable=True)

    @declared_attr
    def created_by(cls):
        return Column(sa.String(32), nullable=True)

    @declared_attr
    def updated_by(cls):
        return Column(sa.String(32), nullable=True)


class DeletedMixin:
    """Mixin for soft delete support"""
    is_deleted = Column(sa.Boolean, default=False, nullable=False)
    delete_reason = Column(sa.String(255), nullable=True)


class RemarkMixin:
    """Mixin for optional remark field"""
    remark = Column(sa.String(255), nullable=True)
