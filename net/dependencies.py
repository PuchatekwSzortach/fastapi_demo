"""
Module with common dependencies
"""

import contextlib
import typing

import sqlalchemy.orm.session

import net.models


@contextlib.contextmanager
def yield_mysql_session():
    """
    Creates mysql session, closes it after yield

    Yields:
        sqlalchemy.orm.session.Session: sqlalchemy instance
    """

    session = net.models.session_maker()

    try:

        yield session

    finally:

        session.close()
