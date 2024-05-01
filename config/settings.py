import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    TITLE = "Users API RESTful"
    VERSION = "0.0.1"
    DESCRIPTION = """
    This is a simple project
    This is not for production

    The methods in this doc are provided for users authentication and some operations such as:
        - Create a new User
        - Verify User's token
        - Update User's data (you must send a valid jwt)
        - Delete User's data (you must send a valid jwt)
        - Get User's info/data (you only can retrieve your own data)

    By Nicolas Delgado
    email: nicolas.delgado.dev@gmail.com

    """
    NAME = "Nicolas Delgado Rios"
    EMAIL = "nicolas.delgado.dev@gmail.com"

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
    POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DATABASE}"


settings = Settings()
