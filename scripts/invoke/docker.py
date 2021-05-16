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
def run(context):
    """
    Run app container

    Args:
        context (invoke.Context): invoke context instance
    """

    import os

    tmp_directory_path = "/tmp/fast_api_demo_tmp"
    os.makedirs(tmp_directory_path, exist_ok=True)

    container_name = "fastapi_demo"

    try:

        command = (
            "docker run -d -t "
            f"--name {container_name} "
            # Attach container to same network as docker-compose set up for backend services
            "-v $PWD:/app:delegated "
            f"-v {tmp_directory_path}:/tmp "
            "-p 8000:8000 "
            "puchatek_w_szortach/fastapi_demo:latest"
        )

        context.run(command, pty=True, echo=True)

        for environment in ["development", "test"]:

            network_name = f"{environment}_fastapi_demo_network"

            command = (
                f"docker network connect {network_name} {container_name}"
            )

            context.run(command, pty=True, echo=True)

        command = (
            f"docker exec -it {container_name} bash"
        )

        context.run(command, pty=True, echo=True)

    finally:

        command = (
            f"docker rm -f {container_name}"
        )

        context.run(command, pty=True, echo=True)


def run_docker_compose_command(context: invoke.Context, environment: str, command: str):
    """
    Run indicated docker compose commmand with settings for specified environment

    Args:
        context (invoke.Context): context instance
        environment (str): environment, one of {development, test}
        command (str): command to run
    """

    valid_environments = {"development", "test"}

    if environment not in valid_environments:
        raise ValueError(f"Invalid environment {environment}, must be one of {valid_environments}")

    env_file_path = f".env.{environment}.env"

    command = f"docker-compose --project-name {environment} --env-file {env_file_path} {command}"
    context.run(command, pty=True, echo=True)


@invoke.task
def compose_up(context, environment):
    """
    Run `docker-compose up` task with specified configuration

    Args:
        context (invoke.Context): context instance
        environment (str): name of environment to use, one of {development, test}
    """

    run_docker_compose_command(
        context=context,
        environment=environment,
        command="up --detach"
    )


@invoke.task
def compose_stop(context, environment):
    """
    Run `docker-compose stop` task with specified configuration

    Args:
        context (invoke.Context): context instance
        environment (str): name of environment to use, one of {development, test}
    """

    run_docker_compose_command(
        context=context,
        environment=environment,
        command="stop"
    )
