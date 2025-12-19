from datetime import datetime
from core.api.api import Api
from service.users_service import UsersService
from database.aio_session import get_async_session
from webapi.schemas.users import UserCreate, UserUpdate

api = Api.get_instance()

# -------------------------------
# GET /users_pages
# -------------------------------
@api.get("users_pages")
async def get_users(
    status: str = None,
    pageindex: int = 0,
    pagesize: int = 10,
    sortby: str = "id",
    descending: int = 0,
):
    async with get_async_session() as session:
        service = UsersService(session)
        users = await service.get_users(
            status=status,
            pageindex=pageindex,
            pagesize=pagesize,
            sortby=sortby,
            descending=bool(descending),
        )
        return users

# -------------------------------
# GET /users/{id}
# -------------------------------
@api.get("users")
async def get_user(user_id: int):
    async with get_async_session() as session:
        service = UsersService(session)
        user = await service.get_user_by_id(user_id)
        if not user:
            return {"error": "User not found"}
        return user.to_dict()

# -------------------------------
# POST /users_create
# -------------------------------
@api.post("users_create")
async def create_user(body: dict):
    async with get_async_session() as session:
        service = UsersService(session)
        new_user = await service.create_user(body)  # Service handles validation & conversion
        return new_user.to_dict()

# -------------------------------
# PUT /users_update
# -------------------------------
@api.put("users_update")
async def update_user(body: dict):
    if "id" not in body:
        return {"error": "Missing user id"}
    async with get_async_session() as session:
        service = UsersService(session)
        updated_user = await service.update_user(body)  # Service handles validation & conversion
        if not updated_user:
            return {"error": "User not found"}
        return updated_user.to_dict()

# -------------------------------
# DELETE /users_delete
# -------------------------------
@api.delete("users_delete")
async def delete_user(body: dict):
    if "id" not in body:
        return {"error": "Missing user id"}
    async with get_async_session() as session:
        service = UsersService(session)
        result = await service.delete_user(body["id"])
        return {"success": result}
