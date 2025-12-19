# OpsPilot Backend

## Project Overview

OpsPilot Backend is a Python-based asynchronous API server built with FastAPI (or your async framework) and SQLAlchemy ORM.  
It provides CRUD operations and business logic for managing users, including features like soft deletion, user updates, and validation using Pydantic models.

---

## Requirements

- Python 3.11+
- PostgreSQL
- Async dependencies listed in `requirements.txt` (e.g., SQLAlchemy, asyncpg, Pydantic)

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/OpsPilot.git
cd OpsPilot/backend
```

2. **Create a virtual environment and activate**

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure database connection**

5. **Run the server**
```bash
python -m core.server.restful_server

```

Directory Structure

```
backend/
├─ src/
│  ├─ webapi/       # API endpoints
│  │  └─ users_api.py
│  ├─ service/      # Business logic layer
│  │  └─ users_service.py
│  ├─ database/     # Async database session
│  ├─ models/       # SQLAlchemy ORM models
│  └─ core/         # API core, server, exceptions
├─ requirements.txt
└─ ...

```

## API Endpoints Example
### Create User

- URL: /api/users_create
- Method: POST 
- Body:

```json
{
"name": "Test",
"age": 28,
"password": "123456",
"birthdate": "1995-08-10",
"sex": 1,
"status_code": "ACTIVE"
}

```


- Response:

```json
{
"id": 1,
"name": "Miffy",
"age": 28,
"birthdate": "1995-08-10",
"sex": 1,
"status_code": "ACTIVE",
"created_at": "2025-12-19T17:00:00",
"updated_at": "2025-12-19T17:00:00"
}
```


### Update User

- URL: /api/users_update
- Method: PUT
- Body:

```json
{
"id": 1,
"age": 29,
"birthdate": "1995-08-15"
}
```


### Delete User

- URL: /api/users_delete
- Method: DELETE
- Body:

```json
{
"id": 1
}
```


### Notes

- All date fields should follow YYYY-MM-DD format.
- Soft deletion is implemented: deleted users will not be returned in queries.
- Validation is handled in the service layer using Pydantic models (UserCreate and UserUpdate).