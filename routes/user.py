# Dependencies
from typing import List

from fastapi import APIRouter, Depends, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy import or_
from sqlalchemy.orm import Session

from config.db import SessionLocal
from middlewares.verify_token_route import VerifyTokenRoute
from models.user import users
from schemas.user import User, UpdateUser
from utils.hashing import fernet, key
from utils.user import verify_token, cast_data_to_dict
from pydantic import EmailStr

users_router = APIRouter(route_class=VerifyTokenRoute)
create_user_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@create_user_router.post(
    "/users/create",
    response_model=User,
    tags=["users"],
    description="Create a new user",
)
def create_user(user: User, db: Session = Depends(get_db)) -> dict:
    """Create a new user endpoint definition.
    To create a new user you must provide the necessary data, such as first_name, last_name,
    email, username and password.

    If there exists another user with the same username OR the same email, then return an error.

    Args:
        user (User): user data passed via JSON body.
        db (Session, optional): db pre-loaded session. Defaults to Depends(get_db).

    Returns:
        dict: new user-info
    """
    # hash the user's password
    print(key)
    user.password = fernet.encrypt(user.password.encode("utf-8")).decode("utf-8")
    _user = users(**user.dict(exclude_none=True))
    # check if the user exists
    is_an_existing_user = (
        db.query(users)
        .filter(or_(users.email == user.email, users.username == user.username))
        .all()
    )
    print(is_an_existing_user)

    # if there exists another user with the same username or email, return an error
    if is_an_existing_user:
        return JSONResponse(
            content={
                "error": "There exists another user with the same username or email"
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    db.add(_user)
    db.commit()
    db.refresh(_user)
    _user = _user.__dict__
    _user.pop("_sa_instance_state")

    return JSONResponse(content=_user, status_code=status.HTTP_201_CREATED)


@create_user_router.get(
    "/users/all",
    tags=["users"],
    response_model=List[User],
    description="Get a list of all users",
)
def get_users(
    db: Session = Depends(get_db),
):
    """Created for testing purposes"""
    return db.query(users).all()


@users_router.get(
    "/users",
    tags=["users"],
    response_model=List[User],
    description="Get the current user info",
)
def get_user_info(
    Authorization: str = Header(None),
    db: Session = Depends(get_db),
):
    """Return the current user info depending on the data in the JWT

    Args:
        Authorization (str, optional): You must send the jwt in the headers. Defaults to Header(None).
        db (Session, optional): pre-load the db session. Defaults to Depends(get_db).

    Returns:
        dict: logged user info
    """
    try:
        user_logged_data = verify_token(Authorization)
        username = user_logged_data.get("username")
        if username:
            user_data = db.query(users).filter(users.username == username).first()
            return JSONResponse(
                content=cast_data_to_dict(user_data), status_code=status.HTTP_200_OK
            )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST
        )


@users_router.put(
    "/users",
    tags=["users"],
    response_model=List[User],
    description="Update the current user info",
)
def update_user_info(
    first_name: str | None = None,
    last_name: str | None = None,
    email: EmailStr | None = None,
    password: str | None = None,
    Authorization: str = Header(None),
    db: Session = Depends(get_db),
):
    """Update the current user info depending on the data in the JWT

    Args:
        first_name (str | None, optional): First name of the user. Defaults to None.
        last_name (str | None, optional): Last name of the user. Defaults to None.
        email (EmailStr | None, optional): Email to update. Defaults to None.
        password (str | None, optional): New password (if needed). Defaults to None.
        Authorization (str, optional): You must send the jwt in the headers. Defaults to Header(None).
        db (Session, optional): pre-load the db session. Defaults to Depends(get_db).

    Returns:
        dict: user-info that has been updated
    """
    try:
        user_logged_data = verify_token(Authorization)
        username = user_logged_data.get("username")
        if username:
            user_data = db.query(users).filter(users.username == username).first()

            if first_name:
                user_data.first_name = first_name
            if last_name:
                user_data.last_name = last_name
            if email:
                user_data.email = email
            if password:
                # encrypt the new password
                user_data.password = fernet.encrypt(password.encode("utf-8")).decode(
                    "utf-8"
                )

            db.commit()
            db.refresh(user_data)
            return JSONResponse(
                content=cast_data_to_dict(user_data), status_code=status.HTTP_200_OK
            )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST
        )


@users_router.delete(
    "/users",
    tags=["users"],
    response_model=List[User],
    description="Get the current user info",
)
def delete_user(
    Authorization: str = Header(None),
    db: Session = Depends(get_db),
):
    """Delete the current user depending on the data in the JWT. The JWT was signed with the username
    So, the account to delete will be the account that generate the given JWT.

    Args:
        Authorization (str, optional): You must send the jwt in the headers. Defaults to Header(None).
        db (Session, optional): pre-load the db session. Defaults to Depends(get_db).
    """
    try:
        user_logged_data = verify_token(Authorization)
        username = user_logged_data.get("username")
        if username:
            user = db.query(users).filter(users.username == username).first()
            user_data = cast_data_to_dict(user)
            db.delete(user)
            db.commit()
            return JSONResponse(content=user_data, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST
        )
