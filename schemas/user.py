from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: Optional[int]
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
