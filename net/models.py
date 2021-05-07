"""
Module with models definitions
"""

import databases
import fastapi_users.db
import fastapi_users.models
import pydantic
import sqlalchemy.ext.declarative

import net.authentication
import net.globals


class User(fastapi_users.models.BaseUser):
    """
    User model
    """

    pass


class UserCreate(User, fastapi_users.models.BaseUserCreate):
    """
    User update model
    """

    pass


class UserUpdate(User, fastapi_users.models.BaseUserUpdate):
    """
    User update model
    """

    pass


class UserDB(User, fastapi_users.models.BaseUserDB):
    """
    Pydantic representation of user in database
    """
    pass


DATABASE_URL = net.globals.CONFIG["database_url"]
database = databases.Database(DATABASE_URL)

Base: sqlalchemy.ext.declarative.DeclarativeMeta = sqlalchemy.ext.declarative.declarative_base()


class UserTable(Base, fastapi_users.db.SQLAlchemyBaseUserTable):
    """
    Sqlalchemy representation of Users ORM class
    """

    pass


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)


Base.metadata.create_all(engine)

user_db = fastapi_users.db.SQLAlchemyUserDatabase(
    user_db_model=UserDB,
    database=database,
    users=UserTable.__table__)


authentication_backends = net.authentication.get_fastapi_users_authentication_backends()

fastapi_users_app = fastapi_users.FastAPIUsers(
    db=user_db,
    auth_backends=authentication_backends,
    user_model=User,
    user_create_model=UserCreate,
    user_update_model=UserUpdate,
    user_db_model=UserDB
)


class ItemPostRequest(pydantic.BaseModel):
    """
    Model for POST items request
    """

    name: str


class ItemResponse(pydantic.BaseModel):
    """
    Model for responses of items related api endpoints
    """

    id: str
    owner_id: str
    name: str
