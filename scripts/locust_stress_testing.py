"""
Script with locust stress testing code for web server
"""

import random

import faker
import locust


class WebsiteUser(locust.HttpUser):
    """
    Class representing a user that locust will imitate during stress testing
    """

    # Set rate at which locust will send requests
    wait_time = locust.constant(0.01)
    token: str
    last_retrievewed_items: list = []

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """

        email = faker.Faker().email()

        # # Register user
        # response = self.client.post(
        #     "register",
        #     json={
        #         "email": email,
        #         "password": "testtest"
        #     }
        # )

        # # Obtain authorization token
        # response = self.client.post("login", data={
        #     "username": email,
        #     "password": "testtest"
        # })

        # assert response.status_code == 200

        # self.token = response.json()["access_token"]

    # @locust.task(weight=1)
    # def post_item(self):
    #     """
    #     Post an item
    #     """

    #     self.client.post(
    #         "items",
    #         headers={"Authorization": f"Bearer {self.token}"},
    #         json={"name": faker.Faker().job()}
    #     )

    # @locust.task(weight=2)
    # def get_items(self):
    #     """
    #     Get all items
    #     """

    #     response = self.client.get(
    #         "items",
    #         headers={"Authorization": f"Bearer {self.token}"}
    #     )

    #     if response.status_code == 200:
    #         self.last_retrievewed_items = response.json()

    # @locust.task(weight=4)
    # def get_item(self):
    #     """
    #     Get one item
    #     """

    #     if len(self.last_retrievewed_items) > 0:

    #         # Choose item id
    #         target_item_id = random.choice(self.last_retrievewed_items)['id']

    #         self.client.get(
    #             f"items/{target_item_id}",
    #             headers={"Authorization": f"Bearer {self.token}"},
    #             name="items/<id>"
            # )

    @locust.task(weight=2)
    def get_public_items(self):
        """
        Get public items
        """

        self.client.get("public_items")
