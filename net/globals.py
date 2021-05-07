"""
Module with globals - because some of them you can't really avoid ><
"""

import os
import functools

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

    return config


CONFIG = get_config()
