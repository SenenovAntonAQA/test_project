import requests
from services.general.helpers.base_helper import BaseHelper


class StudentHelper(BaseHelper):
    ENDPOINT_PREFIX = "/students"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    STUDENT_DETAIL_ENDPOINT = f"{ENDPOINT_PREFIX}/{{student_id}}/"

    def get_students(self) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def post_students(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def delete_student(self, student_id: str) -> requests.Response:
        endpoint = self.STUDENT_DETAIL_ENDPOINT.format(student_id=student_id)
        response = self.api_utils.delete(endpoint)
        return response

    def get_student(self, student_id: str) -> requests.Response:
        endpoint = self.STUDENT_DETAIL_ENDPOINT.format(student_id=student_id)
        response = self.api_utils.get(endpoint)
        return response

    def update_student(self, student_id: str, json: dict) -> requests.Response:
        endpoint = self.STUDENT_DETAIL_ENDPOINT.format(student_id=student_id)
        response = self.api_utils.update(endpoint,json=json)
        return response
