"""
Items routes
"""

import random
import typing

import fastapi

import net.models


router = fastapi.APIRouter()


items = {
    "1": {
        "name": "luggage",
        "id": "1",
        "owner_id": "007"
    },
    "2": {
        "name": "honey",
        "id": "2",
        "owner_id": "13"
    }
}


@router.get("/items", response_model=typing.List[net.models.ItemResponse])
def get_items():
    """
    Get data about all items
    """

    return list(items.values())


@router.get("/items/{item_id}", response_model=net.models.ItemResponse)
def get_selected_item(item_id: str):
    """
    Get data about specified user
    """

    if item_id not in items.keys():

        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND)

    return items[item_id]


@router.post("/items", response_model=net.models.ItemResponse)
def post_user(user_data: net.models.ItemPostRequest):
    """
    Create a new item
    """

    data = user_data.dict()

    # Create id, don't care about keys collisions for now
    data["id"] = str(random.randint(0, 100))

    # Hard code owner id for now
    data["owner_id"] = "007"

    # Create user instance
    item = net.models.ItemResponse(**data)

    # Add user to our "database"
    items[item.id] = item

    # Return response
    return item
