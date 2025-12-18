# webapi/users_api.py

from core.api.api import Api
from service.users_service import UsersService
from database.aio_session import get_async_session

api = Api.get_instance()


# -------------------------------
# GET /users
# -------------------------------
@api.get("users.pages")
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
        # 將 ORM 物件轉成 dict
        print(users)
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
    if "name" not in body or "password" not in body:
        return {"error": "Missing required fields: name or password"}
    async with get_async_session() as session:
        service = UsersService(session)
        new_user = await service.create_user(body)
        return new_user.to_dict()


# -------------------------------
# PUT /users_update
# -------------------------------
@api.put("users_update")
async def update_user(body: dict):
    if "id" not in body:
        return {"error": "Missing user id"}

    # Convert birthdate string to date if present
    from datetime import datetime
    if "birthdate" in body and isinstance(body["birthdate"], str):
        try:
            body["birthdate"] = datetime.strptime(body["birthdate"], "%Y-%m-%d").date()
        except ValueError as e:
            return {"error": f"Invalid birthdate format, must be YYYY-MM-DD: {e}"}

    async with get_async_session() as session:
        service = UsersService(session)
        updated_user = await service.update_user(body)
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
        deleted_user = await service.delete_user(body["id"])
        return deleted_user
