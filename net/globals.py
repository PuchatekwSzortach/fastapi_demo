"""
Module with globals - because some of them you can't really avoid ><
"""

import os
import functools

import pydotenv
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
        f"@{dot_environment['mysql_container_name']}:{dot_environment['mysql_port']}/{config['mysql']['database_name']}"
    )

    return config


CONFIG = get_config()
