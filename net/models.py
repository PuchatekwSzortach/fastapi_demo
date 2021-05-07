"""
Module with models definitions
"""

import pydantic


class UserPostRequest(pydantic.BaseModel):
    """
    Model for POST users request
    """

    name: str
    age: int


class UserResponse(pydantic.BaseModel):
    """
    Model for responses of users related api endpoints
    """

    name: str
    id: str
    age: int
