""""
Module with applications objects builders
"""

import fastapi

import net.models
import net.routes.items
import net.routes.slogans


def get_fastapi_app() -> fastapi.FastAPI:
    """
    Fastapi application builder

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
        net.models.fastapi_users_app.get_auth_router(net.models.fastapi_users_app.authenticator.backends[0]),
        tags=["authentication"]
    )

    app.include_router(
        net.models.fastapi_users_app.get_register_router(
            net.models.PostRegisterHelper(
                database_instance=net.models.database,
                users_table=net.models.UserTable.__table__).on_after_register
        ),
        tags=["authentication"],
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
