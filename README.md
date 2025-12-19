
---

## Full Project README (Frontend + Backend)

# OpsPilot Project

## Project Overview
OpsPilot is a full-stack application for managing users.  
It includes:

- Backend: Python, FastAPI-style custom API layer, Async SQLAlchemy, PostgreSQL
- Frontend: Vue.js + iView UI library
- Features:
    - User CRUD (Create, Read, Update, Delete)
    - Inline editable tables
    - Modal dialogs for add/edit
    - User login functionality
    - Soft-delete for users
    - API validation and error handling

---

## Project Structure

```
OpsPilot/
├─ backend/
│ ├─ src/
│ │ ├─ webapi/ # API endpoints
│ │ │ └─ users_api.py
│ │ ├─ service/ # Business logic layer
│ │ │ └─ users_service.py
│ │ ├─ database/ # Async database session
│ │ ├─ models/ # SQLAlchemy ORM models
│ │ └─ core/ # API core, server, exceptions
│ ├─ requirements.txt
│ └─ ...
├─ frontend/
│ ├─ public/
│ ├─ src/
│ │ ├─ api/
│ │ │ └─ users-api.js
│ │ ├─ components/
│ │ │ └─ tables/
│ │ ├─ view/
│ │ │ └─ Users.vue
│ │ ├─ App.vue
│ │ └─ main.js
│ ├─ package.json
│ └─ ...
└─ README.md

```
---

## Prerequisites

- **Backend**
    - Python >= 3.10
    - PostgreSQL
- **Frontend**
    - Node.js >= 18
    - npm or yarn

---

## Backend Setup

1. Install Python dependencies:

```bash
cd backend
pip install -r requirements.txt
```

2. Configure database connection in database/aio_session.py.
3. Run backend server:
```bash
python -m src.webapi.main
```
- API Base URL: http://localhost:7000/api


## Frontend Setup

1. Install dependencies:

```bash
cd frontend
npm install
# or yarn install

```


2. Run dev server:

```bash
npm run serve
# or yarn serve
```
- Open http://localhost:8080


## API Endpoints

| Method | Endpoint      | Description                |
| ------ | ------------- | -------------------------- |
| GET    | /users_pages  | Fetch paginated users      |
| GET    | /users/{id}   | Fetch user by ID           |
| POST   | /users_create | Create new user            |
| PUT    | /users_update | Update existing user       |
| DELETE | /users_delete | Soft delete user           |
| POST   | /login        | Login user (returns token) |


## Frontend Features

- Editable user table with inline editing
- Add / Edit modal dialogs
- Soft-delete with confirmation
- Search users by name
- Error messages displayed for API failures

## Notes

- Birthdate must be YYYY-MM-DD.
- Sex stored as integer (1 = Male, 2 = Female) but displayed as text.
- Modal validation is handled by backend.
- Password cannot be edited in "Edit User" modal.
- Soft delete sets is_deleted = True without removing the database record.

## Recommended Browser

- Latest Chrome or Edge