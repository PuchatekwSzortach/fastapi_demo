""""
Module with applications objects builders
"""

import fastapi

import net.globals
import net.models
import net.routes.authentication
import net.routes.items
import net.routes.slogans


def get_default_fastapi_app() -> fastapi.FastAPI:
    """
    Fastapi application builder with default settings

    Returns:
        fastapi.FastAPI: configured fastapi app
    """

    return get_configured_fastapi_app(allow_password_login=False)


def get_configured_fastapi_app(allow_password_login: str) -> fastapi.FastAPI:
    """
    Configurable fastapi application builder

    Args:
        allow_password_login (str): if True, then /login route is included

    Returns:
        fastapi.FastAPI: configured fastapi app
    """

    app = fastapi.FastAPI()

    @app.on_event("startup")
    async def startup():
        await net.models.database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await net.models.database.disconnect()

    app.include_router(
        net.models.fastapi_users_app.get_register_router(
            net.models.PostRegisterHelper(
                database_instance=net.models.database,
                users_table=net.models.UserTable.__table__).on_after_register
        ),
        tags=["authentication"],
    )

    if allow_password_login:

        app.include_router(
            net.models.fastapi_users_app.get_auth_router(net.models.fastapi_users_app.authenticator.backends[0]),
            tags=["authentication"]
        )

    # Extended authentication routes
    app.include_router(
        net.routes.authentication.router,
        tags=["authentication"]
    )

    app.include_router(
        net.routes.items.router,
        tags=["items"]
    )

    app.include_router(
        net.routes.slogans.router,
        tags=["slogans"]
    )

    return app
