"""
Tests for fastapi app routes
"""

import fastapi.testclient

import net.applications


def test_foo():
    """
    Simple dummy test
    """

    app = net.applications.get_fastapi_app()
    client = fastapi.testclient.TestClient(app)

    response = client.get("/users")

    assert response.status_code == 200
    assert len(response.json()) > 0
