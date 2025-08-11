import requests
from services.general.helpers.base_helper import BaseHelper


class TeacherHelper(BaseHelper):
    ENDPOINT_PREFIX = "/teachers"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"

    def get_teachers(self) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def post_teachers(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def delete_teacher(self, teacher_id: str) -> requests.Response:
        response = self.api_utils.delete(f"{self.ROOT_ENDPOINT}{teacher_id}/")
        return response

    def get_teacher(self, teacher_id: str) -> requests.Response:
        response = self.api_utils.get(f"{self.ROOT_ENDPOINT}{teacher_id}/")
        return response

    def update_teacher(self, teacher_id: str, json: dict) -> requests.Response:
        response = self.api_utils.update(f"{self.ROOT_ENDPOINT}{teacher_id}/",
                                        json=json)
        return response
