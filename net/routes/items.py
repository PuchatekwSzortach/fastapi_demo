"""
Items routes
"""

import random
import typing

import fastapi
import net.authentication

import net.models


router = fastapi.APIRouter()

# Pitiful excuse of a database ^^;
items = {}


@router.get("/items", response_model=typing.List[net.models.ItemResponse])
def get_items(
    user: net.models.User = fastapi.Depends(net.models.fastapi_users_app.current_user())
):
    """
    Get data about all items
    """

    user_items = [item for item in items.values() if item["owner_id"] == str(user.id)]
    return user_items


@router.get("/items/{item_id}", response_model=net.models.ItemResponse)
def get_selected_item(
        item_id: str,
        user: net.models.User = fastapi.Depends(net.models.fastapi_users_app.current_user())):
    """
    Get data about specified user
    """

    if item_id not in items.keys() or items[item_id]["owner_id"] != str(user.id):

        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND)

    return items[item_id]


@router.post("/items", response_model=net.models.ItemResponse)
def post_item(
        user_data: net.models.ItemPostRequest,
        user: net.models.User = fastapi.Depends(net.models.fastapi_users_app.current_user())):
    """
    Create a new item
    """

    data = user_data.dict()

    # Create id, don't care about keys collisions for now
    data["id"] = str(random.randint(0, 100))

    # Hard code owner id for now
    data["owner_id"] = str(user.id)

    # Create item instance
    item = net.models.ItemResponse(**data)

    # Add item to our "database"
    items[item.id] = item.dict()

    # Return response
    return item
