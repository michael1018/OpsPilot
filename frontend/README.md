# OpsPilot Frontend

## Project Overview
This is the frontend of the OpsPilot project, built with **Vue.js** and **iView UI library**.
It provides a user management interface including:

- View, search, add, edit, and delete users
- Editable tables with inline editing
- Modal dialogs for creating and editing users
- Interaction with backend APIs

---

## Project Structure
```
frontend/
├─ public/ # Static files (favicon, index.html, images)
├─ src/
│ ├─ api/ # API request functions using axios
│ │ └─ users-api.js
│ ├─ components/
│ │ └─ tables/ # Table component for displaying users
│ ├─ view/
│ │ └─ Users.vue # Main user management page
│ ├─ App.vue
│ └─ main.js # Entry point, register plugins
├─ package.json
└─ ...
```

---

## Prerequisites

- Node.js >= 18
- npm or yarn
- Backend API running at `http://localhost:7000/api`

---

## Setup

1. Install dependencies:

```bash
npm install
# or
yarn install
```

2. Run development server:
```bash
npm run serve
# or
yarn serve
```

3. Open browser at http://localhost:8080


### API Integration

- GET /users_pages: Fetch paginated users

- GET /users/{id}: Fetch user by ID

- POST /users_create: Add a new user

- PUT /users_update: Update user

- DELETE /users_delete: Soft delete user

All requests are made via src/api/users-api.js.

### Notes

- Sex is stored as 1 = Male, 2 = Female but displayed as text.

- Birthdate must be in YYYY-MM-DD format.

- Modal form validation is handled by the backend.

- API errors are displayed with this.$Message.error(...).
