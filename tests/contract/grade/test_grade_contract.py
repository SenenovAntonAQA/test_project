import random

import pytest
import requests.status_codes
from faker import Faker

from logger.logger import Logger
from services.university.helpers.grade_helper import GradeHelper
from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.student_helper import StudentHelper
from services.university.helpers.teacher_helper import TeacherHelper
from utils.random_utils import get_grade_random_choice, \
    get_subject_random_choice, generate_russian_phone, get_degree_random_choice

faker = Faker()


class TestCreateGrade:
    def test_create_grade(self, university_api_utils_admin):
        group_helper = GroupHelper(university_api_utils_admin)
        response = group_helper.post_groups(json={"name": faker.name()})
        group_id = response.json()['id']

        student_helper = StudentHelper(university_api_utils_admin)
        response = student_helper.post_students(
            json={"first_name": faker.first_name(),
                  "last_name": faker.last_name(),
                  "email": faker.email(),
                  "degree": get_degree_random_choice(),
                  "phone": generate_russian_phone(),
                  "group_id": group_id})
        student_id = response.json()['id']

        teacher_helper = TeacherHelper(university_api_utils_admin)
        response = teacher_helper.post_teachers(
            json={"first_name": faker.first_name(),
                  "last_name": faker.last_name(),
                  "subject": get_subject_random_choice()}
        )
        teacher_id = response.json()['id']

        grade_helper = GradeHelper(university_api_utils_admin)
        response = grade_helper.post_grades(
            data={"teacher_id": teacher_id,
                  "student_id": student_id,
                  "grade": get_grade_random_choice()})

        assert response.status_code == requests.status_codes.codes.created, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.created}'")

    @pytest.mark.parametrize("grade", [0, 1, 4, 5])
    def test_check_grades_boundary_values(self,
                                          university_api_utils_admin,
                                          grade):
        group_helper = GroupHelper(university_api_utils_admin)
        response = group_helper.post_groups(json={"name": faker.name()})
        group_id = response.json()['id']

        student_helper = StudentHelper(university_api_utils_admin)
        response = student_helper.post_students(
            json={"first_name": faker.first_name(),
                  "last_name": faker.last_name(),
                  "email": faker.email(),
                  "degree": get_degree_random_choice(),
                  "phone": generate_russian_phone(),
                  "group_id": group_id})
        student_id = response.json()['id']

        teacher_helper = TeacherHelper(university_api_utils_admin)
        response = teacher_helper.post_teachers(
            json={"first_name": faker.first_name(),
                  "last_name": faker.last_name(),
                  "subject": get_subject_random_choice()}
        )
        teacher_id = response.json()['id']

        grade_helper = GradeHelper(university_api_utils_admin)
        response = grade_helper.post_grades(
            data={"teacher_id": teacher_id,
                  "student_id": student_id,
                  "grade": grade})

        assert response.json()['grade'] == grade, \
            (f"Wrong grade. Actual: '{response.json()['grade']}', "
             f"but expected: '{grade}'")

    @pytest.mark.parametrize("grade", [-1, 6, 0.5, "5", "good", "A", None, ""])
    def test_check_invalid_values_grade(self,
                                        university_api_utils_admin,
                                        grade):
        group_helper = GroupHelper(university_api_utils_admin)
        response = group_helper.post_groups(json={"name": faker.name()})
        group_id = response.json()['id']

        student_helper = StudentHelper(university_api_utils_admin)
        response = student_helper.post_students(
            json={"first_name": faker.first_name(),
                  "last_name": faker.last_name(),
                  "email": faker.email(),
                  "degree": get_degree_random_choice(),
                  "phone": generate_russian_phone(),
                  "group_id": group_id})
        student_id = response.json()['id']

        teacher_helper = TeacherHelper(university_api_utils_admin)
        response = teacher_helper.post_teachers(
            json={"first_name": faker.first_name(),
                  "last_name": faker.last_name(),
                  "subject": get_subject_random_choice()}
        )
        teacher_id = response.json()['id']

        grade_helper = GradeHelper(university_api_utils_admin)
        response = grade_helper.post_grades(
            data={"teacher_id": teacher_id,
                  "student_id": student_id,
                  "grade": grade})

        assert response.status_code == requests.status_codes.codes.unprocessable, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.unprocessable}'")


class TestGetGradesStats:
    def test_check_grade_stat_null(self,
                                   university_api_utils_admin,
                                   created_teacher,
                                   created_group):
        Logger.info("### Создаем студента")
        student_helper = StudentHelper(university_api_utils_admin)

        response = student_helper.post_students(
            json={"first_name": faker.first_name(),
                  "last_name": faker.last_name(),
                  "email": faker.email(),
                  "degree": get_degree_random_choice(),
                  "phone": generate_russian_phone(),
                  "group_id": created_group})
        student_id = response.json()['id']

        grade_helper = GradeHelper(university_api_utils_admin)
        response = grade_helper.get_grades_stats(student_id=student_id)

        Logger.info("### Проверяем пустые оценки у студента")

        assert response.status_code == requests.status_codes.codes.ok, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.ok}'")

        assert response.json()['count'] == 0, \
            (f"Wrong count. Actual: '{response.json()['count']}', "
             f"but expected: '0'")

        assert response.json()['min'] is None, \
            (f"Wrong min. Actual: '{response.json()['min']}', "
             f"but expected: 'null'")

        assert response.json()['max'] is None, \
            (f"Wrong max. Actual: '{response.json()['max']}', "
             f"but expected: 'null'")

        assert response.json()['avg'] is None, \
            (f"Wrong avg. Actual: '{response.json()['avg']}', "
             f"but expected: 'null'")

    def test_check_grade_stat_student(self,
                                      university_api_utils_admin,
                                      created_teacher,
                                      created_group):
        Logger.info("### Создаем студента и проверяем привязку оценки")
        student_helper = StudentHelper(university_api_utils_admin)

        response = student_helper.post_students(
            json={"first_name": faker.first_name(),
                  "last_name": faker.last_name(),
                  "email": faker.email(),
                  "degree": get_degree_random_choice(),
                  "phone": generate_russian_phone(),
                  "group_id": created_group})
        student_id = response.json()['id']

        grade_helper = GradeHelper(university_api_utils_admin)

        grade = get_grade_random_choice()
        grade_helper.post_grades(data={"teacher_id": created_teacher,
                                       "student_id": student_id,
                                       "grade": grade})

        response = grade_helper.get_grades_stats(student_id=student_id)

        assert response.status_code == requests.status_codes.codes.ok, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.ok}'")

        assert response.json()['count'] == 1, \
            (f"Wrong count. Actual: '{response.json()['count']}', "
             f"but expected: '1'")

        assert response.json()['min'] == grade, \
            (f"Wrong min. Actual: '{response.json()['min']}', "
             f"but expected: 'null'")

        assert response.json()['max'] == grade, \
            (f"Wrong max. Actual: '{response.json()['max']}', "
             f"but expected: 'null'")

        assert response.json()['avg'] == grade, \
            (f"Wrong avg. Actual: '{response.json()['avg']}', "
             f"but expected: 'null'")

    def test_check_count_grade_of_group(self,
                                        university_api_utils_admin,
                                        created_teacher,
                                        created_group):
        Logger.info("### Генерируем список из 5 студентов одной группы,"
                    " которым проставим оценки")
        student_ids = []
        student_helper = StudentHelper(university_api_utils_admin)
        for _ in range(5):
            response = student_helper.post_students(
                json={"first_name": faker.first_name(),
                      "last_name": faker.last_name(),
                      "email": faker.email(),
                      "degree": get_degree_random_choice(),
                      "phone": generate_russian_phone(),
                      "group_id": created_group})
            student_ids.append(response.json()['id'])

        grades = []
        grade_helper = GradeHelper(university_api_utils_admin)
        for student_id in student_ids:
            response = grade_helper.post_grades(
                data={"teacher_id": created_teacher,
                      "student_id": student_id,
                      "grade": get_grade_random_choice()})
            grades.append(response.json()['grade'])

        response = grade_helper.get_grades_stats(group_id=created_group)

        assert response.json()['count'] == len(grades), \
            (f"Incorrect сount. Actual: '{response.json()['count']}",
             f" but expected: '{len(grades)}'")

    def test_check_count_grade_of_teacher(self,
                                          university_api_utils_admin,
                                          created_teacher):
        Logger.info("### Создаем 3 группы по 3 студента, которые учатся у "
                    "одного препода")

        group_helper = GroupHelper(university_api_utils_admin)
        student_helper = StudentHelper(university_api_utils_admin)

        student_ids = []

        for i in range(3):

            response = group_helper.post_groups(json={
                "name": "test_grades" + faker.name()})
            group_id = response.json()["id"]
            for j in range(3):
                response = student_helper.post_students(
                    json={"first_name": faker.first_name(),
                          "last_name": faker.last_name(),
                          "email": faker.email(),
                          "degree": get_degree_random_choice(),
                          "phone": generate_russian_phone(),
                          "group_id": group_id})
                student_ids.append(response.json()['id'])

        grade_helper = GradeHelper(university_api_utils_admin)
        for student_id in student_ids:
            grade_helper.post_grades(data={"teacher_id": created_teacher,
                                           "student_id": student_id,
                                           "grade": get_grade_random_choice()})

        Logger.info("### Проверяем привязку к преподу")

        response = grade_helper.get_grades_stats(teacher_id=created_teacher)

        assert response.json()['count'] == len(student_ids), \
            (f"Incorrect сount. Actual: '{response.json()['count']}",
             f" but expected: '{len(student_ids)}'")

    def test_check_grade_stat_of_teacher_group(self,
                                               university_api_utils_admin,
                                               created_teacher):
        Logger.info("### Создаем 3 группы по 3 студента, которые учатся у "
                    "одного препода")

        group_helper = GroupHelper(university_api_utils_admin)
        student_helper = StudentHelper(university_api_utils_admin)

        group_ids = []
        student_ids = {}
        for i in range(3):

            response = group_helper.post_groups(json={
                "name": "test_grades" + faker.name()})
            group_id = response.json()["id"]
            group_ids.append(group_id)
            for j in range(3):
                response = student_helper.post_students(
                    json={"first_name": faker.first_name(),
                          "last_name": faker.last_name(),
                          "email": faker.email(),
                          "degree": get_degree_random_choice(),
                          "phone": generate_russian_phone(),
                          "group_id": group_id})
                if group_id not in student_ids:
                    student_ids[group_id] = [response.json()['id']]
                else:
                    student_ids[group_id].append(response.json()['id'])

        grade_helper = GradeHelper(university_api_utils_admin)
        for ids in student_ids.values():
            for student_id in ids:
                grade_helper.post_grades(data={"teacher_id": created_teacher,
                                               "student_id": student_id,
                                               "grade": get_grade_random_choice()})

        Logger.info("### Проверяем привязку к преподe и группе")

        group_id = random.choice(group_ids)
        response = grade_helper.get_grades_stats(teacher_id=created_teacher,
                                                 group_id=group_id)

        assert response.json()['count'] == len(student_ids[group_id]), \
            (f"Incorrect сount. Actual: '{response.json()['count']}",
             f" but expected: '{len(student_ids[group_id])}'")
