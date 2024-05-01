from sqlalchemy import Column, Integer, String

from config.db import Base


class users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    username = Column(String)
    password = Column(String)


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

# meta.create_all(engine)
