from dotenv import load_dotenv
from fastapi import FastAPI

from config.db import engine
from config.settings import settings
from models.user import Base
from routes.auth import auth_routes
from routes.user import create_user_router, users_router

app = FastAPI(
    title=settings.TITLE,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    contact={"name": settings.NAME, "email": settings.EMAIL},
    redoc_url="/documentation",
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_routes, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(create_user_router, prefix="/api")
load_dotenv()
