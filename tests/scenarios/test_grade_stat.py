import random

import requests.status_codes
from faker import Faker

from pytest_check import check
from logger.logger import Logger
from services.university.models.grade_request import GradeRequest
from services.university.university_service import UniversityService
from utils.data_generators import generate_groups_and_students
from utils.random_utils import get_grade_random_choice

faker = Faker()


class TestGetGradesStats:
    def test_check_grade_stat_null(self,
                                   university_api_utils_admin,
                                   created_student):
        university_service = UniversityService(
            api_utils=university_api_utils_admin)
        response = university_service.get_grade_stat(student_id=created_student)

        Logger.info("### Проверяем пустые оценки у студента")

        check.equal(response.count, 0,
                    (f"Wrong count. Actual: '{response.count}', "
                     f"but expected: '0'"))

        check.is_none(response.min,
                      (f"Wrong min. Actual: '{response.min}', "
                       f"but expected: 'null'"))

        check.is_none(response.max,
                      (f"Wrong max. Actual: '{response.max}', "
                       f"but expected: 'null'"))

        check.is_none(response.avg,
                      (f"Wrong avg. Actual: '{response.avg}', "
                       f"but expected: 'null'"))

    def test_check_grade_stat_student(self,
                                      university_api_utils_admin,
                                      created_teacher,
                                      created_student):
        university_service = UniversityService(
            api_utils=university_api_utils_admin)

        Logger.info("### Step 1. Создаем и привязываем оценку к студенту")
        grade = get_grade_random_choice()
        grade_request = GradeRequest(teacher_id=created_teacher,
                                     student_id=created_student,
                                     grade=grade)
        university_service.create_grade(grade_request)

        Logger.info("### Step 2. Проверяем статистику по студенту")

        response = university_service.get_grade_stat(student_id=created_student)

        check.equal(response.count, 1,
                    (f"Wrong count. Actual: '{response.count}', "
                     f"but expected: '1'"))

        check.equal(response.min, grade,
                    (f"Wrong min. Actual: '{response.min}', "
                     f"but expected: 'null'"))

        check.equal(response.max, grade,
                    (f"Wrong max. Actual: '{response.max}', "
                     f"but expected: 'null'"))

        check.equal(response.avg, grade,
                    (f"Wrong avg. Actual: '{response.avg}', "
                     f"but expected: 'null'"))

    def test_check_count_grade_of_group(self,
                                        university_api_utils_admin,
                                        created_teacher):
        Logger.info("### Генерируем список из 5 студентов одной группы,"
                    " которым проставим оценки")
        group_student_ids = generate_groups_and_students(
            students=5, groups=1, api_utils=university_api_utils_admin)

        Logger.info("### Проставляем всем оценки у одного препода")

        grades = []

        university_service = UniversityService(university_api_utils_admin)

        for student_ids in list(group_student_ids.values()):
            for student_id in student_ids:
                grade_response = university_service.create_grade(GradeRequest(
                    teacher_id=created_teacher,
                    student_id=student_id,
                    grade=get_grade_random_choice()))
                grades.append(grade_response.grade)

        Logger.info("### Проверяем статистику оценок группы")

        group_id = random.choice(group_student_ids.keys())
        stat_response = university_service.get_grade_stat(group_id=group_id)

        assert stat_response.count == len(grades), \
            (f"Incorrect сount. Actual: '{stat_response.count}",
             f" but expected: '{len(grades)}'")

    def test_check_count_grade_of_teacher(self,
                                          university_api_utils_admin,
                                          created_teacher):
        Logger.info("### Создаем 3 группы по 3 студента, которые учатся у "
                    "одного препода")

        group_student_ids = generate_groups_and_students(
            students=3, groups=3, api_utils=university_api_utils_admin)

        Logger.info("### Step 2. Присваиваем оценки всем студентам из 3 групп")

        university_service = UniversityService(university_api_utils_admin)

        for student_ids in list(group_student_ids.values()):
            for student_id in student_ids:
                university_service.create_grade(GradeRequest(
                    teacher_id=created_teacher,
                    student_id=student_id,
                    grade=get_grade_random_choice()))

        Logger.info("### Проверяем привязку только к преподу")

        stat_response = university_service.get_grade_stat(
            teacher_id=created_teacher)

        assert stat_response.count == len(group_student_ids.values()), \
            (f"Incorrect сount. Actual: '{stat_response.count}",
             f" but expected: '{len(group_student_ids.values())}'")

    def test_check_grade_stat_of_teacher_group(self,
                                               university_api_utils_admin,
                                               created_teacher):
        Logger.info("### Создаем 3 группы по 3 студента, которые учатся у "
                    "одного препода")

        group_student_ids = generate_groups_and_students(
            students=3, groups=3, api_utils=university_api_utils_admin)

        Logger.info("### Проставляем всем оценки у одного препода")

        university_service = UniversityService(university_api_utils_admin)

        for student_ids in list(group_student_ids.values()):
            for student_id in student_ids:
                university_service.create_grade(GradeRequest(
                    teacher_id=created_teacher,
                    student_id=student_id,
                    grade=get_grade_random_choice()))

        Logger.info("### Проверяем привязку к преподу и конкретной группе")
        print(group_student_ids.keys())
        group_id = random.choice(list(group_student_ids.keys()))

        stat_response = university_service.get_grade_stat(
            teacher_id=created_teacher, group_id=group_id)

        assert stat_response.count == len(group_student_ids[group_id]), \
            (f"Incorrect сount. Actual: '{stat_response.count}",
             f" but expected: '{len(group_student_ids[group_id])}'")
