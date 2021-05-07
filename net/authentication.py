"""
Module with authentication logic
"""

import fastapi_users
import fastapi_users.authentication


def get_fastapi_users_authentication_backends() -> list:
    """
    Get fastapi users authentication backends

    Args:
        config (dict): configuration

    Returns:
        list: authentication backends
    """

    authentication_backends = [
        fastapi_users.authentication.JWTAuthentication(
            secret="dummy secret",
            lifetime_seconds=3600
        )
    ]

    return authentication_backends
