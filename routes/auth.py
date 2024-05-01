from fastapi import APIRouter, Depends, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config.db import SessionLocal
from functions_jwt import validate_token, write_token
from schemas.user import UserLogin
from utils.hashing import fernet, key
from utils.user import get_user_info

auth_routes = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@auth_routes.post(
    "/login",
    tags=["Login"],
    description="Login with username and password to generate a valid JWT",
)
def login(user: UserLogin, db: Session = Depends(get_db)) -> str:
    user_info = get_user_info(user, db)
    user_password = user_info.get("password")

    # if there exists an user with the same username, then check the password
    if user_info:
        # if the password encrypted in db is the same as user-input-password, then generate jwt
        # throw an error otherwise
        if fernet.decrypt(user_password).decode("utf-8") == user.password:
            user_dict = user.dict()
            # delete password to sign the jwt only with username
            user_dict.pop("password")
            return JSONResponse(
                content={"token": write_token(user_dict)},
                status_code=status.HTTP_200_OK,
            )
        return JSONResponse(
            content={
                "error": "Incorrect username or password, please check your credentials and try again"
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    else:
        return JSONResponse(
            content={"message": "User not found"}, status_code=status.HTTP_404_NOT_FOUND
        )


@auth_routes.post(
    "/verify/token",
    tags=["Login"],
    description="Endpoint to verify the autenticity of a JWT",
)
def verify_token(Authorization: str = Header(None)):
    if not Authorization:
        return JSONResponse(
            content={"error": "Bad request"}, status_code=status.HTTP_400_BAD_REQUEST
        )
    token = Authorization.split(" ")[1]
    return validate_token(token, output=True)
