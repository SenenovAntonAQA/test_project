import requests
from services.general.helpers.base_helper import BaseHelper


class GroupHelper(BaseHelper):
    ENDPOINT_PREFIX = "/groups"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    GROUP_DETAIL_ENDPOINT = f"{ENDPOINT_PREFIX}/{{group_id}}/"

    def get_groups(self) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def post_groups(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def delete_group(self, group_id: int) -> requests.Response:
        endpoint = self.GROUP_DETAIL_ENDPOINT.format(group_id=group_id)
        response = self.api_utils.delete(endpoint)
        return response

    def get_group(self, group_id: int) -> requests.Response:
        endpoint = self.GROUP_DETAIL_ENDPOINT.format(group_id=group_id)
        response = self.api_utils.get(endpoint)
        return response

    def update_group(self, group_id: int, json: dict) -> requests.Response:
        endpoint = self.GROUP_DETAIL_ENDPOINT.format(group_id=group_id)
        response = self.api_utils.update(endpoint, json=json)
        return response
