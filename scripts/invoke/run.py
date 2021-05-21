"""
Tasks to run most common processes
"""

import invoke


@invoke.task
def web(context):
    """
    Run web server
    """

    command = "uvicorn --factory net.applications:get_default_fastapi_app --host 0.0.0.0 --reload"

    context.run(
        command,
        echo=True,
        env={
            "CONFIG_PATH": "./configurations/development.yaml",
            "PYTHONUNBUFFERED": "1"
        }
    )


@invoke.task
def alembic(context):
    """
    Run web server
    """

    config_path = "./configurations/development.yaml"

    import os
    os.environ["CONFIG_PATH"] = config_path

    import sqlalchemy_utils.functions

    import net.globals

    url = net.globals.CONFIG["mysql_connection_string"]

    if not sqlalchemy_utils.functions.database_exists(url=url):

        sqlalchemy_utils.functions.create_database(url=url)

    command = "alembic upgrade head"
    context.run(command, echo=True)
