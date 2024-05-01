from datetime import datetime, timedelta, timezone
from os import getenv

from fastapi import status
from fastapi.responses import JSONResponse
from jwt import decode, encode, exceptions


def expire_date(seconds: int = 360, kwargs={}):
    """Function that creates the ttl offset for the jwt.

    Args:
        seconds (int): the time in seconds that has the user
            to make granted requests using the jwt. Defaults to 15.
        kwargs (dict, optional): another optional params
            such as mins or hours. Defaults to {}.

    Returns:
        (datetime): the current time (in UTC-timezone)
            adding the extra time delta.
    """
    now = datetime.now(timezone.utc)
    new_date = now + timedelta(seconds=seconds, **kwargs)
    return new_date


def write_token(data: dict, kwargs: dict = {}):
    """Method to create the JWT signed with custom data.

    Args:
        data (dict): custom data to sign the jwt.
        kwargs (dict, optional): additional arguments to
            set the jwt ttl. Defaults to {}.

    Returns:
        str: signed and encoded jwt with ttl=15seconds
            by default, or custom if needed.
    """
    ttl = expire_date(kwargs=kwargs)
    token = encode(
        payload={**data, "exp": ttl}, key=getenv("SECRET_KEY"), algorithm="HS256"
    )
    return token


def validate_token(token: str, output=False):
    """Method that verify the jwt autenticity.

    Args:
        token (str): token (as str) to verify
        output (bool, optional): return flag to
            return the decoded data. Defaults to False.

    Returns:
        (dict): return the decoded data if output flag is true.
            If there's an invalid token, then raise a 401 with invalid token message.
            If there's an expired token, then raise a 401 with expired token message.
    """
    try:
        if output:
            return decode(token, key=getenv("SECRET_KEY"), algorithms=["HS256"])
        decode(token, key=getenv("SECRET_KEY"), algorithms=["HS256"])
    except exceptions.DecodeError:
        return JSONResponse(
            content={"message": "Invalid Token"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    except exceptions.ExpiredSignatureError:
        return JSONResponse(
            content={"message": "Token Expired"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
