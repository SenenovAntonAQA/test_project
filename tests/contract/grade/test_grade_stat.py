import requests.status_codes

from logger.logger import Logger
from services.university.helpers.grade_helper import GradeHelper
from utils.random_utils import get_grade_random_choice


class TestGetGradesStats:
    def test_check_grade_stat_null(self,
                                   university_api_utils_admin,
                                   created_student):
        grade_helper = GradeHelper(api_utils=university_api_utils_admin)
        response = grade_helper.get_grades_stats(student_id=created_student)

        assert response.status_code == requests.status_codes.codes.ok, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.ok}'")

    def test_check_grade_stat_student(self,
                                      university_api_utils_admin,
                                      created_teacher,
                                      created_student):
        grade_helper = GradeHelper(api_utils=university_api_utils_admin)


        Logger.info("### Step 1. Создаем и привязываем оценку к студенту")

        grade_helper.post_grades(data={
            "student_id": created_student,
            "teacher_id": created_teacher,
            "grade": get_grade_random_choice()
        })

        Logger.info("### Step 2. Проверяем статистику по студенту")

        response = grade_helper.get_grades_stats(student_id=created_student)

        assert response.status_code == requests.status_codes.codes.ok, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.ok}'")