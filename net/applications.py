""""
Module with applications objects builders
"""

import fastapi

import net.routes.users


def get_fastapi_app() -> fastapi.FastAPI:
    """
    Fastapi application builder

    Returns:
        fastapi.FastAPI: configured fastapi app
    """

    app = fastapi.FastAPI()

    app.include_router(net.routes.users.router)

    return app
