"""
Module with models definitions
"""

import pydantic


class UserResponse(pydantic.BaseModel):

    name: str
    id: str
    age: int
