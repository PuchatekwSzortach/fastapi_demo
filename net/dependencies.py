"""
Module with common dependencies
"""

import sqlalchemy.orm.session

import net.models


def yield_mysql_session() -> sqlalchemy.orm.session.Session:
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
