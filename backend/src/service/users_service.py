from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.users import Users
from typing import Optional
from datetime import datetime
from webapi.schemas.users import UserCreate, UserUpdate

class UsersService:
    """
    UsersService uses async SQLAlchemy session to perform CRUD operations on the Users table.
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
        filters = []

        if status:
            filters.append(Users.status_code == status)

        query = select(Users)
        if filters:
            query = query.where(*filters)

        query = query.where(Users.is_deleted == deleted)

        column = getattr(Users, sortby, None)
        if column:
            query = query.order_by(column.desc() if descending else column.asc())

        query = query.limit(pagesize).offset(pageindex * pagesize)

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
        # Convert birthdate string to date
        if "birthdate" in data and isinstance(data["birthdate"], str):
            try:
                data["birthdate"] = datetime.fromisoformat(data["birthdate"][:10]).date()
            except ValueError:
                raise ValueError("Invalid birthdate format, must be YYYY-MM-DD")

        # Validate input using Pydantic
        user_in = UserCreate(**data)

        # Check if user already exists
        stmt = select(Users).where(Users.name == user_in.name)
        result = await self.session.execute(stmt)
        if result.scalars().first():
            raise ValueError("User already exists")

        user = Users(**user_in.dict())
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
        stmt = select(Users).where(Users.id == user_id, Users.is_deleted == False)
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        if not user:
            return None

        # Convert birthdate string to date
        if "birthdate" in data and isinstance(data["birthdate"], str):
            try:
                data["birthdate"] = datetime.fromisoformat(data["birthdate"][:10]).date()
            except ValueError:
                raise ValueError("Invalid birthdate format, must be YYYY-MM-DD")

        # Validate input using Pydantic
        user_in = UserUpdate(**data)

        # Update attributes
        for key, value in user_in.dict(exclude_unset=True).items():
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
        stmt = select(Users).where(Users.id == user_id, Users.is_deleted == False)
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        if not user:
            return False

        user.is_deleted = True
        user.updated_at = datetime.utcnow()
        self.session.add(user)
        await self.session.commit()
        return True
