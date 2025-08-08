import requests
from services.general.helpers.base_helper import BaseHelper


class GroupHelper(BaseHelper):
    ENDPOINT_PREFIX = "/groups"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"

    def get_groups(self) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def post_groups(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def delete_group(self, group_id: str) -> requests.Response:
        response = self.api_utils.delete(f"self.ROOT_ENDPOINT{group_id}/")
        return response

    def get_group(self, group_id: str) -> requests.Response:
        response = self.api_utils.get(f"self.ROOT_ENDPOINT{group_id}/")
        return response

    def update_group(self, group_id: str, json: dict) -> requests.Response:
        response = self.api_utils.update(f"self.ROOT_ENDPOINT{group_id}/",
                                        json=json)
        return response
