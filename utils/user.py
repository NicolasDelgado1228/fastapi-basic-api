from functions_jwt import validate_token
from fastapi import status

from sqlalchemy.orm import Session
from models.user import users
from schemas.user import UserLogin


def cast_data_to_dict(query):
    if not query:
        return {}

    query = query.__dict__
    query.pop("_sa_instance_state")
    return query


def get_user_info(user: UserLogin, db: Session):
    _user = db.query(users).filter(users.username == user.username).first()
    return cast_data_to_dict(_user)


def verify_token(Authorization):
    if not Authorization:
        raise Exception("Bad request")
    token = Authorization.split(" ")[1]
    return validate_token(token, output=True)
