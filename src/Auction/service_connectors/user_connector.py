import os
import requests


class UserConnector:
    def __init__(self):
        if not os.getenv("USER_SERVICE_ADDRESS"):
            raise ValueError("USER_SERVICE_ADDRESS environment variable not set")
        self.user_service_address = os.getenv("USER_SERVICE_ADDRESS")

    def add_item_to_shopping_cart(self, user_id, item_id):
        response = requests.post(f"{self.user_service_address}/api/users/cart/{user_id}",
                                 json={ "item_id": item_id})
        return response.json()