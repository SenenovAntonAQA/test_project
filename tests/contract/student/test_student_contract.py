import random

import pytest
import requests
from faker import Faker

from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.student_helper import StudentHelper
from utils.random_utils import (generate_invalid_names,
                                get_degree_random_choice,
                                generate_russian_phone,
                                generate_invalid_email,
                                generate_invalid_groups,
                                generate_invalid_group_ids,
                                generate_unique_group_id)

faker = Faker()


class TestCreateStudent:
    def test_create_student(self, university_api_utils_admin, created_group):
        student_helper = StudentHelper(university_api_utils_admin)
        response = student_helper.post_students(
            json={"first_name": faker.first_name(),
                  "last_name": faker.last_name(),
                  "email": faker.email(),
                  "degree": get_degree_random_choice(),
                  "phone": generate_russian_phone(),
                  "group_id": created_group})

        assert response.status_code == requests.status_codes.codes.created, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.created}'")

    @pytest.mark.parametrize("invalid_f_name", generate_invalid_names())
    def test_create_student_with_invalid_f_name(self,
                                                university_api_utils_admin,
                                                invalid_f_name,
                                                created_group):
        student_helper = StudentHelper(university_api_utils_admin)
        response = student_helper.post_students(
            json={"first_name": invalid_f_name,
                  "last_name": faker.last_name(),
                  "email": faker.email(),
                  "degree": get_degree_random_choice(),
                  "phone": generate_russian_phone(),
                  "group_id": created_group})

        assert response.status_code == requests.status_codes.codes.unprocessable, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.unprocessable}'")

    @pytest.mark.parametrize("invalid_l_name", generate_invalid_names())
    def test_create_student_with_invalid_l_name(self,
                                                university_api_utils_admin,
                                                invalid_l_name,
                                                created_group):
        student_helper = StudentHelper(university_api_utils_admin)
        response = student_helper.post_students(
            json={"first_name": faker.first_name(),
                  "last_name": invalid_l_name,
                  "email": faker.email(),
                  "degree": get_degree_random_choice(),
                  "phone": generate_russian_phone(),
                  "group_id": created_group})

        assert response.status_code == requests.status_codes.codes.unprocessable, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.unprocessable}'")

    @pytest.mark.parametrize("invalid_email", generate_invalid_email())
    def test_create_student_with_invalid_email(self,
                                               university_api_utils_admin,
                                               invalid_email,
                                               created_group):
        student_helper = StudentHelper(university_api_utils_admin)
        response = student_helper.post_students(
            json={"first_name": faker.first_name(),
                  "last_name": faker.last_name(),
                  "email": invalid_email,
                  "degree": get_degree_random_choice(),
                  "phone": generate_russian_phone(),
                  "group_id": created_group})

        assert response.status_code == requests.status_codes.codes.unprocessable, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.unprocessable}'")

    @pytest.mark.parametrize("group_id", generate_invalid_groups())
    def test_create_student_with_invalid_group(self,
                                               university_api_utils_admin,
                                               group_id):
        student_helper = StudentHelper(university_api_utils_admin)
        response = student_helper.post_students(
            json={"first_name": faker.first_name(),
                  "last_name": faker.last_name(),
                  "email": faker.email(),
                  "degree": get_degree_random_choice(),
                  "phone": generate_russian_phone(),
                  "group_id": group_id})

        assert response.status_code == requests.status_codes.codes.unprocessable, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.unprocessable}'")

    def test_create_student_not_found_group(self, university_api_utils_admin):
        group_helper = GroupHelper(university_api_utils_admin)
        response = group_helper.get_groups()
        groups = response.json()
        group_ids = [group["id"] for group in groups]

        student_helper = StudentHelper(university_api_utils_admin)
        response = student_helper.post_students(
            json={"first_name": faker.first_name(),
                  "last_name": faker.last_name(),
                  "email": faker.email(),
                  "degree": get_degree_random_choice(),
                  "phone": generate_russian_phone(),
                  "group_id": generate_unique_group_id(group_ids)})

        assert response.status_code == requests.status_codes.codes.not_found, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.not_found}'")


class TestUpdateStudent:
    def test_update_student_phones(self, university_api_utils_admin,
                                   created_group):
        student_helper = StudentHelper(university_api_utils_admin)

        payload = {"first_name": faker.first_name(),
                   "last_name": faker.last_name(),
                   "email": faker.email(),
                   "degree": get_degree_random_choice(),
                   "phone": generate_russian_phone(),
                   "group_id": created_group}

        response = student_helper.post_students(json=payload)
        student_id = response.json()['id']

        upd_payload = payload.copy()
        upd_payload["phone"] = generate_russian_phone()

        response = student_helper.update_student(student_id=student_id,
                                                 json=upd_payload)

        assert response.status_code == requests.status_codes.codes.ok, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.ok}'")

    def test_update_to_invalid_email_status_code(self,
                                     university_api_utils_admin,
                                     created_group):
        student_helper = StudentHelper(university_api_utils_admin)

        response = student_helper.get_students()
        students = response.json()
        emails = [student["email"] for student in students]

        payload = {"first_name": faker.first_name(),
                   "last_name": faker.last_name(),
                   "email": faker.email(),
                   "degree": get_degree_random_choice(),
                   "phone": generate_russian_phone(),
                   "group_id": created_group}

        response = student_helper.post_students(json=payload)
        student_id = response.json()['id']

        upd_payload = payload.copy()
        upd_payload["email"] = random.choice(emails)

        response = student_helper.update_student(student_id=student_id,
                                                 json=upd_payload)

        assert response.status_code == requests.status_codes.codes.conflict, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.conflict}'")

    def test_update_to_invalid_email_details(self,
                                     university_api_utils_admin,
                                     created_group):
        student_helper = StudentHelper(university_api_utils_admin)

        response = student_helper.get_students()
        students = response.json()
        emails = [student["email"] for student in students]

        payload = {"first_name": faker.first_name(),
                   "last_name": faker.last_name(),
                   "email": faker.email(),
                   "degree": get_degree_random_choice(),
                   "phone": generate_russian_phone(),
                   "group_id": created_group}

        response = student_helper.post_students(json=payload)
        student_id = response.json()['id']

        upd_payload = payload.copy()
        upd_payload["email"] = random.choice(emails)

        response = student_helper.update_student(student_id=student_id,
                                                 json=upd_payload)

        assert response.json()['detail'] == "Email is already taken", \
            (f"Incorrect actual error text: '{response.json()['detail']}', "
             "expected: 'Email is already taken'")
