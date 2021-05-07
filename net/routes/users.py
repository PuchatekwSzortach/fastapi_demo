"""
Users routes
"""

import random
import typing

import fastapi

import net.models


router = fastapi.APIRouter()


users = {
    "007": {
        "name": "Kuba",
        "id": "007",
        "age": 33
    },
    "13": {
        "name": "Puchatek",
        "id": "13",
        "age": 3
    }
}


@router.get("/users/self", response_model=net.models.UserResponse)
def get_user_self():
    """
    Get data about authenticated user
    """

    return users["007"]


@router.get("/users", response_model=typing.List[net.models.UserResponse])
def get_users():
    """
    Get data about all users
    """

    return list(users.values())


@router.get("/users/{user_id}", response_model=net.models.UserResponse)
def get_selected_user(user_id: str):
    """
    Get data about specified user
    """

    if user_id not in users.keys():

        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND)

    return users[user_id]


@router.post("/users", response_model=net.models.UserResponse)
def post_user(user_data: net.models.UserPostRequest):
    """
    Create a new user
    """

    data = user_data.dict()

    # Create id, don't care about keys collisions for now
    data["id"] = str(random.randint(0, 100))

    # Create user instance
    user = net.models.UserResponse(**data)

    # Add user to our "database"
    users[user.id] = user

    # Return response
    return user
