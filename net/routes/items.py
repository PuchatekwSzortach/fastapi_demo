"""
Items routes
"""

import random
import time
import typing
import uuid

import fastapi
import sqlalchemy
import starlette.status

import net.authentication
import net.dependencies
import net.models


router = fastapi.APIRouter()


@router.get("/public_items", response_model=typing.List[net.models.ItemResponse])
def get_public_items(
    # session_context: sqlalchemy.orm.session.Session = fastapi.Depends(net.dependencies.yield_mysql_session)
):
    """
    Get data about all items
    """

    with net.dependencies.yield_mysql_session() as session:

        # Simulate slow requests
        time.sleep(random.randint(0, 4))

        items = session.query(net.models.ItemsTable).offset(random.randint(0, 100)).limit(100).all()

        return items


@router.get("/items", response_model=typing.List[net.models.ItemResponse])
def get_items(
    user: net.models.User = fastapi.Depends(net.models.fastapi_users_app.current_user()),
    # session_context: sqlalchemy.orm.session.Session = fastapi.Depends(net.dependencies.yield_mysql_session)
):
    """
    Get data about all items
    """

    # with session_context as session:
    with net.dependencies.yield_mysql_session() as session:

        # Simulate slow requests
        time.sleep(random.randint(0, 4))

        items = session.query(net.models.ItemsTable).filter(
            net.models.ItemsTable.owner_id == str(user.id)
        ).all()

        return items


@router.get("/items/{item_id}", response_model=net.models.ItemResponse)
def get_selected_item(
        item_id: str,
        user: net.models.User = fastapi.Depends(net.models.fastapi_users_app.current_user()),
        # session_context: sqlalchemy.orm.session.Session = fastapi.Depends(net.dependencies.yield_mysql_session)
):
    """
    Get data about specified user
    """

    # with session_context as session:
    with net.dependencies.yield_mysql_session() as session:

        # Simulate slow requests
        time.sleep(random.randint(0, 4))

        item = session.query(net.models.ItemsTable).filter(
            net.models.ItemsTable.owner_id == str(user.id),
            net.models.ItemsTable.id == item_id,
        ).one_or_none()

        if item is None:
            raise fastapi.HTTPException(status_code=starlette.status.HTTP_404_NOT_FOUND)

        return item


@router.post("/items", response_model=net.models.ItemResponse, status_code=201)
def post_item(
        item_data: net.models.ItemPostRequest,
        user: net.models.User = fastapi.Depends(net.models.fastapi_users_app.current_user()),
        # session_context: sqlalchemy.orm.session.Session = fastapi.Depends(net.dependencies.yield_mysql_session)
):
    """
    Create a new item
    """

    # with session_context as session:
    with net.dependencies.yield_mysql_session() as session:

        # Simulate slow requests
        time.sleep(random.randint(0, 4))

        database_item = net.models.ItemsTable(
            id=str(uuid.uuid4()),
            owner_id=str(user.id),
            name=item_data.name
        )

        # Create response instance
        item = net.models.ItemResponse.from_orm(database_item)

        session.add(database_item)
        session.commit()

        # Return response
        return item
