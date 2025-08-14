import requests
from services.general.helpers.base_helper import BaseHelper


def _clean_payload(**kwargs) -> dict:
    return {k: v for k, v in kwargs.items() if v is not None}


class GradeHelper(BaseHelper):
    ENDPOINT_PREFIX = "/grades"
    STAT_PREFIX = "/stats"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    STAT_ENDPOINT = f"{ENDPOINT_PREFIX}{STAT_PREFIX}/"
    GRADE_DETAIL_ENDPOINT = f"{ENDPOINT_PREFIX}/{{grade_id}}/"

    def get_grades(self, student_id: int = None, teacher_id: int = None,
                   group_id: int = None, ) -> requests.Response:
        payload = {key: value
                   for key, value in {"student_id": student_id,
                                      "teacher_id": teacher_id,
                                      "group_id": group_id}.items()
                   if value is not None}
        response = self.api_utils.get(self.ROOT_ENDPOINT, params=payload)
        return response

    def post_grades(self, data: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, data=data)
        return response

    def delete_grade(self, grade_id: str) -> requests.Response:
        endpoint = self.GRADE_DETAIL_ENDPOINT.format(grade_id=grade_id)
        response = self.api_utils.delete(endpoint)
        return response

    def get_grades_stats(self, student_id: int = None, teacher_id: int = None,
                         group_id: int = None, ) -> requests.Response:
        payload = {key: value
                   for key, value in {"student_id": student_id,
                                      "teacher_id": teacher_id,
                                      "group_id": group_id}.items()
                   if value is not None}
        response = self.api_utils.get(self.STAT_ENDPOINT, params=payload)
        return response

    def update_grade(self, grade_id: str, data: dict) -> requests.Response:
        endpoint = self.GRADE_DETAIL_ENDPOINT.format(grade_id=grade_id)
        response = self.api_utils.put(endpoint, data=data)
        return response
