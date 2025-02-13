import os
import requests

class ItemConnector:
    def __init__(self):
        if not os.getenv("ITEM_SERVICE_ADDRESS"):
            raise ValueError("ITEM_SERVICE_ADDRESS environment variable not set")
        self.item_service_address = os.getenv("ITEM_SERVICE_ADDRESS")

    def get_item_by_id(self, item_id):
        response = requests.get(f"{self.item_service_address}/items/{item_id}")

        return response.json()

    def update_item(self, item_id, item):
        response = requests.put(f"{self.item_service_address}/items/{item_id}", json=item)

        return response.json()
