# OpsPilot Database Layer Overview

This document outlines the structure and dependencies of the OpsPilot async database layer.

---

## Directory Structure

database/
├── orm.py
│ ├─ Defines ModelBase (SQLAlchemy declarative_base)
│ ├─ Defines AuditMixin, DeletedMixin, RemarkMixin
│ └─ Used by other modules to inherit ORM models
│
├── aio_session.py
│ ├─ AsyncSessionFactory (asyncpg + SQLAlchemy)
│ ├─ ScopeSession
│ │ ├─ select() -> Query (read operations)
│ │ ├─ add() -> ORM write
│ │ ├─ update() -> WriteQuery
│ │ └─ delete() -> WriteQuery
│ └─ Query / WriteQuery: chainable query interface
│
├── aio_api.py
│ ├─ CRUD operations wrapper (add, find, fetch, fetch_pages, update, delete, restore)
│ ├─ Depends on:
│ │ ├─ ModelBase (from orm.py)
│ │ └─ scope_session (from aio_session.py)
│ └─ Helper: ensure_list()
│
└── query_builder.py
├─ Similar functionality to Query / WriteQuery
├─ Chainable SQL builder
└─ Can be used for custom queries

aio_api.py
├── uses ModelBase (orm.py)
└── uses scope_session (aio_session.py)

aio_session.py
└── independent, provides async DB session & chainable queries

query_builder.py
└── optional, used for custom query building (not directly used by aio_api.py)


---

## Flow Overview

1. **orm.py**: Provides ORM base and mixins.
2. **aio_session.py**: Provides async SQLAlchemy session and chainable query/write operations.
3. **aio_api.py**: Provides simple CRUD wrappers for business layer usage.
4. **query_builder.py**: Optional module for advanced custom queries; not used by `aio_api.py`.

---

