from dotenv import load_dotenv
from fastapi import FastAPI

from config.settings import settings
from routes.auth import auth_routes
from routes.user import users_router

# from models.user import

app = FastAPI(
    title=settings.TITLE,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    contact={"name": settings.NAME, "email": settings.EMAIL},
    redoc_url="/documentation",
)

models.Base.metadata.create_all(bind=engine)

app.include_router(auth_routes, prefix="/api")
app.include_router(users_router, prefix="/api")
load_dotenv()
