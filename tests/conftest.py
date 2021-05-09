"""
Base module for pytest fixtures
"""

import os

import fastapi.testclient
import pytest

import net.applications
import net.globals
import net.models


@pytest.fixture(scope="session")
def test_config() -> dict:
    """
    Get test configuration

    Returns:
        dict: test configuration
    """

    os.environ["CONFIG_PATH"] = "./configurations/test.yaml"
    return net.globals.get_config()


@pytest.fixture(scope="function", name="initialize_services")
def fixture_initialize_services():
    """
    Initialize services:
    - delete users data
    """

    # Delete users table data
    session = net.models.session_maker()
    session.query(net.models.UserTable).delete()
    session.commit()


@pytest.fixture(scope="function")
def bootstrap_user_data(initialize_services) -> tuple[fastapi.testclient.TestClient, str]:
    """
    Bootstrap user data:
    - registers user
    - obtains authentication token for user
    - creates a few items

    Returns:
        tuple[fastapi.testclient.TestClient, str]: test client for the app, access token for registered user
    """

    app = net.applications.get_fastapi_app()
    client = fastapi.testclient.TestClient(app)

    response = client.post(
        "/register",
        json={
            "email": "kuba@buba.com",
            "password": "testtest"
        }
    )

    response = client.post("/login", data={
        "username": "kuba@buba.com",
        "password": "testtest"
    })

    access_token = response.json()["access_token"]

    items = [
        {"name": "carrots", "age": "10"},
        {"name": "beans", "age": "20"},
        {"name": "eggs", "age": "1000"}
    ]

    for item in items:

        response = client.post(
            "/items",
            json=item,
            headers={"Authorization": f"Bearer {access_token}"}
        )

        assert response.status_code == 201

    return client, access_token
