"""
Users routes
"""

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

    return users[user_id]
