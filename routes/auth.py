from fastapi import APIRouter, Header, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr

from functions_jwt import validate_token, write_token

auth_routes = APIRouter()


# TODO: migrate the model to models folder
class User(BaseModel):
    username: str
    email: EmailStr


@auth_routes.post("/login")
def login(user: User) -> str:
    # print(user.dict())
    # TODO: check in db if the user exists, then generate a custom jwt
    if user.username == "nikito":
        return JSONResponse(
            content={"token": write_token(user.dict())},
            status_code=status.HTTP_200_OK,
        )
    else:
        return JSONResponse(
            content={"message": "User not found"}, status_code=status.HTTP_404_NOT_FOUND
        )


@auth_routes.post("/verify/token")
def verify_token(Authorization: str = Header(None)):
    if not Authorization:
        return JSONResponse(
            content={"error": "Bad request"}, status_code=status.HTTP_400_BAD_REQUEST
        )
    token = Authorization.split(" ")[1]
    return validate_token(token, output=True)
