"""
Items routes
"""

import random
import typing

import fastapi
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
import net.authentication

import net.models


router = fastapi.APIRouter()


@router.get("/items", response_model=typing.List[net.models.ItemResponse])
def get_items(
    user: net.models.User = fastapi.Depends(net.models.fastapi_users_app.current_user())
):
    """
    Get data about all items
    """

    session = net.models.session_maker()

    items = session.query(net.models.ItemsTable).filter(
        net.models.ItemsTable.owner_id == str(user.id)
    ).all()

    return items


@router.get("/items/{item_id}", response_model=net.models.ItemResponse)
def get_selected_item(
        item_id: str,
        user: net.models.User = fastapi.Depends(net.models.fastapi_users_app.current_user())):
    """
    Get data about specified user
    """

    session = net.models.session_maker()

    item = session.query(net.models.ItemsTable).filter(
        net.models.ItemsTable.owner_id == str(user.id),
        net.models.ItemsTable.id == item_id,
    ).one_or_none()

    if item is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)

    return item


@router.post("/items", response_model=net.models.ItemResponse, status_code=201)
def post_item(
        item_data: net.models.ItemPostRequest,
        user: net.models.User = fastapi.Depends(net.models.fastapi_users_app.current_user())):
    """
    Create a new item
    """

    session = net.models.session_maker()

    database_item = net.models.ItemsTable(
        id=str(random.randint(0, 1000)),
        owner_id=str(user.id),
        name=item_data.name
    )

    # Create response instance
    item = net.models.ItemResponse.from_orm(database_item)

    session.add(database_item)
    session.commit()

    # Return response
    return item
