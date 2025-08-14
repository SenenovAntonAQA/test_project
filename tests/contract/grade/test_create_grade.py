import pytest
import requests.status_codes
from faker import Faker

from services.university.helpers.grade_helper import GradeHelper
from utils.random_utils import get_grade_random_choice

faker = Faker()


class TestCreateGrade:
    def test_create_grade(self,
                          university_api_utils_admin,
                          created_student,
                          created_teacher):
        grade_helper = GradeHelper(university_api_utils_admin)
        response = grade_helper.post_grades(
            data={"teacher_id": created_teacher,
                  "student_id": created_student,
                  "grade": get_grade_random_choice()})

        assert response.status_code == requests.status_codes.codes.created, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.created}'")

    @pytest.mark.parametrize("grade", [0, 1, 4, 5])
    def test_check_grades_boundary_values(self,
                                          university_api_utils_admin,
                                          created_student,
                                          created_teacher,
                                          grade):
        grade_helper = GradeHelper(university_api_utils_admin)
        response = grade_helper.post_grades(
            data={"teacher_id": created_teacher,
                  "student_id": created_student,
                  "grade": grade})

        assert response.json()['grade'] == grade, \
            (f"Wrong grade. Actual: '{response.json()['grade']}', "
             f"but expected: '{grade}'")

    @pytest.mark.parametrize("grade", [-1, 6, 0.5, "5", "good", "A", None, ""])
    def test_check_invalid_values_grade(self,
                                        university_api_utils_admin,
                                        created_student,
                                        created_teacher,
                                        grade):
        grade_helper = GradeHelper(university_api_utils_admin)
        response = grade_helper.post_grades(
            data={"teacher_id": created_teacher,
                  "student_id": created_student,
                  "grade": grade})

        assert response.status_code == requests.status_codes.codes.unprocessable, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.unprocessable}'")