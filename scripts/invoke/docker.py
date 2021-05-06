"""
Module with docker commands
"""

import invoke


@invoke.task
def build_app_container(context):
    """
    Build app container

    :param context: invoke.Context instance
    """

    command = (
        "DOCKER_BUILDKIT=1 docker build "
        "--tag puchatek_w_szortach/fastapi_demo:latest "
        "-f ./docker/app.Dockerfile ."
    )

    context.run(command, echo=True)


@invoke.task
def run(context, config_path):
    """
    Run app container

    Args:
        context (invoke.Context): invoke context instance
        config_path (str): path to configuration file
    """

    command = (
        "docker run -it --rm "
        # Attach container to same network as docker-compose set up for backend services
        "-v $PWD:/app:delegated "
        "-p 8000:8000 "
        "puchatek_w_szortach/fastapi_demo:latest /bin/bash"
    )

    context.run(command, pty=True, echo=True)
