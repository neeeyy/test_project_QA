import requests


class Api:
    def __init__(self, baseurl):
        self.baseurl = baseurl

    def create_item(self, payload):
        response = requests.post(f"{self.baseurl}/api/1/item", json=payload)
        return response

    def get_item_id(self, item_id):
        response = requests.get(f"{self.baseurl}/api/1/item/{item_id}")
        return response

    def get_item_statistics(self, item_id):
        response = requests.get(f"{self.baseurl}/api/2/statistic/{item_id}")
        return response

    def get_user_items(self, seller_id):
        response = requests.get(f"{self.baseurl}/api/1/{seller_id}/item")
        return response
