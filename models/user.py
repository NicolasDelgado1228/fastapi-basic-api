from sqlalchemy import Column, Integer, String  # , Table
from sqlalchemy.ext.declarative import declarative_base
from config.db import engine, meta

Base = declarative_base()


class users(Base):
    __tablename__ = "users"

    Column("id", Integer, primary_key=True, autoincrement=True)
    Column("username", String)
    Column("first_name", String)
    Column("last_name", String)
    Column("email", String)
    Column("password", String)


# users = Table(
#     "users",
#     meta,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("username", String(255)),
#     Column("first_name", String(255)),
#     Column("last_name", String(255)),
#     Column("email", String(255)),
#     Column("password", String(255)),
# )

meta.create_all(engine)
