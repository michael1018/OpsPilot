# webapi/auth_api.py
from datetime import datetime
from core.api.api import Api
from database.aio_session import get_async_session
from sqlalchemy import select
from models.users import Users
from pydantic import BaseModel, Field

api = Api.get_instance()


# -------------------------------
# Pydantic model for login
# -------------------------------
class LoginRequest(BaseModel):
    name: str
    password: str


class LoginResponse(BaseModel):
    id: int
    name: str
    status_code: str | None = None


# -------------------------------
# POST /login
# -------------------------------
@api.post("login")
async def login(body: dict):
    try:
        login_data = LoginRequest(**body)
    except Exception as e:
        return {"error": f"Invalid input: {e}"}

    async with get_async_session() as session:
        query = select(Users).where(
            Users.name == login_data.name,
            Users.password == login_data.password,
            Users.is_deleted == False,
        )
        result = await session.execute(query)
        user = result.scalars().first()

        if not user:
            return {"error": "Invalid username or password"}

        return LoginResponse(
            id=user.id,
            name=user.name,
            status_code=user.status_code
        ).dict()
