from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    # id: Optional[int] = None
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str


class UpdateUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
