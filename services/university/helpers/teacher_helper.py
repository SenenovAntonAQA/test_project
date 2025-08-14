import requests
from services.general.helpers.base_helper import BaseHelper


class TeacherHelper(BaseHelper):
    ENDPOINT_PREFIX = "/teachers"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    TEACHER_DETAIL_ENDPOINT = f"{ENDPOINT_PREFIX}/{{teacher_id}}/"

    def get_teachers(self) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def post_teachers(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def delete_teacher(self, teacher_id: str) -> requests.Response:
        endpoint = self.TEACHER_DETAIL_ENDPOINT.format(teacher_id=teacher_id)
        response = self.api_utils.delete(endpoint)
        return response

    def get_teacher(self, teacher_id: str) -> requests.Response:
        endpoint = self.TEACHER_DETAIL_ENDPOINT.format(teacher_id=teacher_id)
        response = self.api_utils.get(endpoint)
        return response

    def update_teacher(self, teacher_id: str, json: dict) -> requests.Response:
        endpoint = self.TEACHER_DETAIL_ENDPOINT.format(teacher_id=teacher_id)
        response = self.api_utils.update(endpoint,json=json)
        return response
