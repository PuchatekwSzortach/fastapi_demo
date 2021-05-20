"""
Module with globals - because some of them you can't really avoid ><
"""

import functools
import os

import pydotenv
import sqlalchemy_utils.functions
import yaml


@functools.lru_cache
def get_config() -> dict:
    """
    Get configuration, requires CONFIG_PATH environment variable to be set

    Returns:
        dict: configuration
    """

    with open(os.environ["CONFIG_PATH"]) as file:

        config = yaml.safe_load(file)

    # Load environment variables
    dot_environment = pydotenv.Environment(file_path=config["environment_variables_file"])

    config["mysql_connection_string"] = (
        f"mysql://root:{dot_environment['mysql_password']}"
        f"@{dot_environment['mysql_container_name']}:3306/{config['mysql']['database_name']}"
    )

    # It's very dirty to create database in get_config.
    # This is just a temporary solution until we can hopefully move this responsibility to alembic
    if not sqlalchemy_utils.functions.database_exists(url=config["mysql_connection_string"]):

        sqlalchemy_utils.functions.create_database(
            url=config["mysql_connection_string"]
        )

    return config


CONFIG = get_config()
