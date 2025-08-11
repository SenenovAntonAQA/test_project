import requests
from services.general.helpers.base_helper import BaseHelper


class GradeHelper(BaseHelper):
    ENDPOINT_PREFIX = "/grades"
    STAT_PREFIX = "/stats"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    STAT_ENDPOINT = f"{ENDPOINT_PREFIX}{STAT_PREFIX}/"

    def get_grades(self, student_id: int = None, teacher_id: int = None,
                   group_id: int = None, ) -> requests.Response:
        payload = {"student_id": student_id,
                   "teacher_id": teacher_id,
                   "group_id": group_id}
        response = self.api_utils.get(self.ROOT_ENDPOINT, params=payload)
        return response

    def post_grades(self, data: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, data=data)
        return response

    def delete_grade(self, grade_id: str) -> requests.Response:
        response = self.api_utils.delete(f"{self.ROOT_ENDPOINT}{grade_id}/")
        return response

    def get_grades_stats(self, student_id: int = None, teacher_id: int = None,
                         group_id: int = None, ) -> requests.Response:
        payload = {"student_id": student_id,
                   "teacher_id": teacher_id,
                   "group_id": group_id}
        response = self.api_utils.get(self.STAT_ENDPOINT, params=payload)
        return response

    def update_grade(self, grade_id: str, data: dict) -> requests.Response:
        response = self.api_utils.put(f"{self.ROOT_ENDPOINT}{grade_id}/",
                                      data=data)
        return response
