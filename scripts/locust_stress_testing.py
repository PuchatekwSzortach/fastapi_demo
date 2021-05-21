"""
Script with locust stress testing code for web server
"""

import faker
import locust


class WebsiteUser(locust.HttpUser):
    """
    Class representing a user that locust will imitate during stress testing
    """

    # Set rate at which locust will send requests
    wait_time = locust.constant(1)
    token: str

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """

        email = faker.Faker().email()

        # Register user
        response = self.client.post(
            "register",
            json={
                "email": email,
                "password": "testtest"
            }
        )

        # Obtain authorization token
        response = self.client.post("login", data={
            "username": email,
            "password": "testtest"
        })

        assert response.status_code == 200

        self.token = response.json()["access_token"]

    @locust.task
    def get_items(self):
        """
        Send positive/negative prediction and gradient request
        """

        self.client.get(
            "items",
            headers={"Authorization": f"Bearer {self.token}"}
        )

    @locust.task
    def post_item(self):
        """
        Send positive/negative prediction and gradient request
        """

        self.client.post(
            "items",
            headers={"Authorization": f"Bearer {self.token}"},
            json={"name": faker.Faker().job()}
        )
