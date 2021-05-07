"""
Module with models definitions
"""

import pydantic


class UserResponse(pydantic.BaseModel):
    """
    Model for responses of users related api endpoints
    """

    name: str
    id: str
    age: int
