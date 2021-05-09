"""
Tests for fastapi app routes
"""


def test_get_items(bootstrap_user_data):
    """
    Test GET /items endpoint
    """

    client, access_token = bootstrap_user_data

    response = client.get(
        "/items",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_item_with_invalid_id(bootstrap_user_data):
    """
    Test GET /items/{item_id} endpoint with invalid id
    """

    client, access_token = bootstrap_user_data

    response = client.get(
        "/items/dummy_id",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 404
