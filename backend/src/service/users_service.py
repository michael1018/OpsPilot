# service/users_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from models.users import Users
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UsersService:
    """
    UsersService uses async SQLAlchemy session to perform CRUD operations on Users table.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    # -------------------------
    # Read: Get multiple users
    # -------------------------
    async def get_users(
        self,
        *,
        status: Optional[str] = None,
        deleted: bool = False,
        sortby: str = "id",
        descending: bool = False,
        pageindex: int = 0,
        pagesize: int = 10,
    ):
        criterions = []

        # Add status filter
        if status:
            criterions.append(Users.status_code == status)

        # Build base query
        query = select(Users)

        # Add conditions
        if criterions:
            query = query.where(*criterions)

        # Add deleted filter
        query = query.where(Users.is_deleted == deleted)

        # Add sorting
        column = getattr(Users, sortby, None)
        if column:
            query = query.order_by(column.desc() if descending else column.asc())

        # Add pagination
        query = query.limit(pagesize).offset(pageindex * pagesize)

        # Execute query
        result = await self.session.execute(query)
        users = result.scalars().all()
        return [u.to_dict() for u in users]

    # -------------------------
    # Read: Get single user by ID
    # -------------------------
    async def get_user_by_id(self, user_id: int) -> Optional[Users]:
        query = select(Users).where(Users.id == user_id, Users.is_deleted == False)
        result = await self.session.execute(query)
        return result.scalars().first()

    # -------------------------
    # Create: Add a new user
    # -------------------------
    async def create_user(self, data: dict) -> Users:
        # -------------------------------
        # Convert 'birthdate' string to date if necessary
        # -------------------------------
        from datetime import datetime, date
        if "birthdate" in data and isinstance(data["birthdate"], str):
            try:
                data["birthdate"] = datetime.strptime(data["birthdate"], "%Y-%m-%d").date()
            except ValueError as e:
                raise ValueError(f"Invalid birthdate format, must be YYYY-MM-DD: {e}")

        # -------------------------------
        # Check if name already exists
        # -------------------------------
        stmt = select(Users).where(
            Users.name == data["name"]
        )
        result = await self.session.execute(stmt)
        if result.scalars().first():
            raise ValueError("User already exists")

        # -------------------------------
        # Create new user
        # -------------------------------
        user = Users(
            name=data["name"],
            age=data.get("age"),
            password=data["password"],
            birthdate=data.get("birthdate"),
            sex=data.get("sex"),
            status_code=data.get("status_code"),
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

        # -------------------------
        # Update: Update user by ID
        # -------------------------

    async def update_user(self, data: dict) -> Optional[Users]:
        if "id" not in data:
            raise ValueError("Missing user id")

        user_id = data["id"]
        query = select(Users).where(Users.id == user_id, Users.is_deleted == False)
        result = await self.session.execute(query)
        user = result.scalars().first()

        if not user:
            return None

        # -------------------------------
        # Convert birthdate string to date if present
        # -------------------------------
        if "birthdate" in data and isinstance(data["birthdate"], str):
            try:
                data["birthdate"] = datetime.strptime(data["birthdate"], "%Y-%m-%d").date()
            except ValueError as e:
                raise ValueError(f"Invalid birthdate format, must be YYYY-MM-DD: {e}")

        # -------------------------------
        # Update attributes
        # -------------------------------
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        user.updated_at = datetime.utcnow()
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

        # -------------------------
        # Delete: Soft delete user by ID
        # -------------------------

    async def delete_user(self, user_id: int) -> bool:
        query = select(Users).where(Users.id == user_id, Users.is_deleted == False)
        result = await self.session.execute(query)
        user = result.scalars().first()

        if not user:
            return False

        user.is_deleted = True
        user.updated_at = datetime.utcnow()
        self.session.add(user)
        await self.session.commit()
        return True
