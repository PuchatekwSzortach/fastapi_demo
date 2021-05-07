"""
Tests for fastapi app routes
"""

import fastapi.testclient

import net.applications


def test_get_users():
    """
    Test GET /users endpoint
    """

    app = net.applications.get_fastapi_app()
    client = fastapi.testclient.TestClient(app)

    response = client.get("/users")

    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_user_with_invalid_id():
    """
    Test GET /users/{user_id} endpoint with invalid id
    """

    app = net.applications.get_fastapi_app()
    client = fastapi.testclient.TestClient(app)

    response = client.get("/users/dummy_id")

    assert response.status_code == 404
