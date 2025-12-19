# schemas/user.py
from datetime import date
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name: str
    age: int | None = Field(None, ge=0)
    password: str
    birthdate: date | None = None
    sex: int | None = None
    status_code: str | None = None

class UserUpdate(BaseModel):
    id: int
    name: str | None = None
    age: int | None = Field(None, ge=0)
    password: str | None = None
    birthdate: date | None = None
    sex: int | None = None
    status_code: str | None = None