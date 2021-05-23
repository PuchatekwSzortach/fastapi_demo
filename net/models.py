"""
Module with models definitions
"""

import uuid
import typing

import databases
import fastapi
import fastapi_users
import fastapi_users.db
import fastapi_users.models
import pydantic
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

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

    uniquifier: typing.Optional[str]


DATABASE_URL = net.globals.CONFIG["mysql_connection_string"]


database = databases.Database(DATABASE_URL)

Base: sqlalchemy.ext.declarative.DeclarativeMeta = sqlalchemy.ext.declarative.declarative_base()


class UserTable(Base, fastapi_users.db.SQLAlchemyBaseUserTable):
    """
    Sqlalchemy representation of Users ORM class
    """

    uniquifier = sqlalchemy.Column(sqlalchemy.String(length=36), nullable=True)


class ItemsTable(Base):
    """
    Simple items table
    """

    __tablename__ = "items"

    id = sqlalchemy.Column(sqlalchemy.String(length=36), primary_key=True)
    owner_id = sqlalchemy.Column(sqlalchemy.String(length=36), nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String(length=256), nullable=False)


engine = sqlalchemy.create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=0,
    pool_recycle=120,  # seconds after which inactive connection is recycled
    pool_timeout=10  # seconds after which request for new connection times out
)


session_maker = sqlalchemy.orm.sessionmaker(bind=engine)


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

    class Config:
        """
        Config
        """
        orm_mode = True


class PostRegisterHelper:
    """
    Class wrapping up fastapi_users on after register callback
    """

    def __init__(self, database_instance, users_table) -> None:

        self.database = database_instance
        self.users_table = users_table

    async def on_after_register(self, user: UserDB, request: fastapi.Request):
        """
        Updates user's uniquifier field
        """

        query = self.users_table.update().where(self.users_table.c.id == user.id).values(
            {"uniquifier": str(uuid.uuid4())}
        )

        await self.database.execute(query)
