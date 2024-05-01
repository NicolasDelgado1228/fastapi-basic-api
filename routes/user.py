# Dependencies
from cryptography.fernet import Fernet
from fastapi import APIRouter, status
from sqlalchemy import or_

from config.db import conn
from fastapi.responses import JSONResponse
from middlewares.verify_token_route import VerifyTokenRoute
from models.user import users
from schemas.user import User
from typing import List

users_router = APIRouter()  # route_class=VerifyTokenRoute)
key = Fernet.generate_key()
# create a fernet hashing class
fernet = Fernet(key=key)


@users_router.post("/users/create")
def create_user(user: User) -> dict:
    # check if the user exists
    is_an_existing_user = conn.execute(
        users.select().where(
            or_(users.c.username == user.username, users.c.email == user.email)
        )
    ).fetchall()

    # if there exists another user with the same username or email, return an error
    if is_an_existing_user:
        return JSONResponse(
            content={
                "error": "There exists another user with the same username or email"
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # hash the user's password
    user.password = fernet.encrypt(user.password.encode("utf-8")).decode("utf-8")
    inserted_cursor = conn.execute(users.insert().values(user.dict()))
    created_user = conn.execute(
        users.select().where(users.c.id == inserted_cursor.lastrowid)
    ).first()
    return JSONResponse(
        content={"created_user": created_user._asdict()},
        status_code=status.HTTP_201_CREATED,
    )


@users_router.get(
    "/users",
    tags=["users"],
    response_model=List[User],
    description="Get a list of all users",
)
def get_users():
    return conn.execute(users.select()).fetchall()
