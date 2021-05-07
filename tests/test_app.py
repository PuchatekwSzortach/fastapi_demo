"""
Tests for fastapi app routes
"""

import fastapi.testclient

import net.applications


def test_get_items():
    """
    Test GET /items endpoint
    """

    app = net.applications.get_fastapi_app()
    client = fastapi.testclient.TestClient(app)

    response = client.get("/items")

    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_item_with_invalid_id():
    """
    Test GET /items/{item_id} endpoint with invalid id
    """

    app = net.applications.get_fastapi_app()
    client = fastapi.testclient.TestClient(app)

    response = client.get("/items/dummy_id")

    assert response.status_code == 404
