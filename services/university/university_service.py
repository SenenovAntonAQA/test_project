from services.general.base_service import BaseService
from services.general.models.http_validation_error import HTTPValidationError
from services.general.models.success_response import SuccessResponse
from services.university.helpers.grade_helper import GradeHelper
from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.student_helper import StudentHelper
from services.university.helpers.teacher_helper import TeacherHelper
from services.university.models.grade_request import GradeRequest
from services.university.models.grade_response import GradeResponse, \
    GradeStatisticResponse
from services.university.models.group_request import GroupRequest
from services.university.models.group_response import GroupResponse
from services.university.models.student_request import StudentRequest
from services.university.models.student_response import StudentResponse
from services.university.models.teacher_request import TeacherRequest
from services.university.models.teacher_response import TeacherResponse
from utils.api_utils import ApiUtils


class UniversityService(BaseService):
    SERVICE_URL = "http://127.0.0.1:8001"

    def __init__(self, api_utils: ApiUtils):
        super().__init__(api_utils)

        self.group_helper = GroupHelper(self.api_utils)
        self.student_helper = StudentHelper(self.api_utils)
        self.teacher_helper = TeacherHelper(self.api_utils)
        self.grade_helper = GradeHelper(self.api_utils)

    def create_group(self,
                     group_request: GroupRequest) -> GroupResponse:
        response = self.group_helper.post_groups(
            json=group_request.model_dump())
        return GroupResponse(**response.json())

    def create_student(self,
                       student_request: StudentRequest) -> StudentResponse:
        response = self.student_helper.post_students(
            json=student_request.model_dump())
        return StudentResponse(**response.json())

    def delete_student(self, student_id) -> SuccessResponse:
        response = self.student_helper.delete_student(student_id=student_id)
        return SuccessResponse(**response.json())

    def get_student(self,student_id):
        response = self.student_helper.get_student(student_id=student_id)
        if response.status_code == 200:
            return StudentResponse(**response.json())
        elif response.status_code == 404:
            return SuccessResponse(**response.json())
        elif response.status_code == 422:
            return HTTPValidationError(**response.json())

    def create_teacher(self,
                       teacher_request: TeacherRequest) -> TeacherResponse:
        response = self.teacher_helper.post_teachers(
            json=teacher_request.model_dump())
        return TeacherResponse(**response.json())

    def update_teacher(self,
                       teacher_id,
                       teacher_request: TeacherRequest) -> TeacherResponse:
        response = self.teacher_helper.update_teacher(
            teacher_id=teacher_id,
            json=teacher_request.model_dump())
        return TeacherResponse(**response.json())

    def teacher_info(self, teacher_id) -> TeacherResponse:
        response = self.teacher_helper.get_teacher(teacher_id=teacher_id)
        return TeacherResponse(**response.json())

    def create_grade(self,
                     grade_request: GradeRequest) -> GradeResponse:
        response = self.grade_helper.post_grades(
            data=grade_request.model_dump())
        return GradeResponse(**response.json())

    def get_grade_stat(self,student_id: int = None, teacher_id: int = None,
    group_id: int = None,) -> GradeStatisticResponse:
        response = self.grade_helper.get_grades_stats(
            student_id=student_id, teacher_id=teacher_id, group_id=group_id)
        return GradeStatisticResponse(**response.json())