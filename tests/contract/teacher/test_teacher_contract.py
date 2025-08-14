import requests.status_codes
from faker import Faker

from services.university.helpers.teacher_helper import TeacherHelper
from utils.random_utils import get_subject_random_choice

faker = Faker()


class TestCreateTeacher:
    def test_create_teacher_anonym(self, university_api_utils_anonym):
        teacher_helper = TeacherHelper(university_api_utils_anonym)
        response = teacher_helper.post_teachers(
            json={"first_name": faker.first_name(),
                  "last_name": faker.last_name(),
                  "subject": get_subject_random_choice()}
        )

        assert response.status_code == requests.status_codes.codes.unauthorized, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.unauthorized}'")

    def test_create_teacher_invalid_token(self,
                                          university_api_utils_invalid_token):
        teacher_helper = TeacherHelper(university_api_utils_invalid_token)
        response = teacher_helper.post_teachers(
            json={"first_name": faker.first_name(),
                  "last_name": faker.last_name(),
                  "subject": get_subject_random_choice()}
        )

        assert response.status_code == requests.status_codes.codes.unauthorized, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.unauthorized}'")

    def test_create_teacher_admin(self, university_api_utils_admin):
        teacher_helper = TeacherHelper(university_api_utils_admin)
        response = teacher_helper.post_teachers(
            json={"first_name": faker.first_name(),
                  "last_name": faker.last_name(),
                  "subject": get_subject_random_choice()}
        )

        assert response.status_code == requests.status_codes.codes.created, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.created}'")


class TestUpdateTeacher:
    def test_update_f_name_teacher(self, university_api_utils_admin):
        teacher_helper = TeacherHelper(university_api_utils_admin)

        last_name = faker.last_name()
        subject = get_subject_random_choice()
        response = teacher_helper.post_teachers(
            json={"first_name": faker.first_name(),
                  "last_name": last_name,
                  "subject": subject})

        response = teacher_helper.update_teacher(
            teacher_id=response.json()['id'],
            json={"first_name": faker.first_name(),
                  "last_name": last_name,
                  "subject": subject})

        assert response.status_code == requests.status_codes.codes.ok, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.ok}'")


class TestDeleteTeacher:
    def test_delete_teacher_status_code(self, university_api_utils_admin):
        teacher_helper = TeacherHelper(university_api_utils_admin)
        response = teacher_helper.post_teachers(
            json={"first_name": faker.first_name(),
                  "last_name": faker.last_name(),
                  "subject": get_subject_random_choice()}
        )

        response = teacher_helper.delete_teacher(response.json()['id'])

        assert response.status_code == requests.status_codes.codes.ok, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.ok}'")

    def test_delete_teacher_error_text(self, university_api_utils_admin):
        teacher_helper = TeacherHelper(university_api_utils_admin)
        response = teacher_helper.post_teachers(
            json={"first_name": faker.first_name(),
                  "last_name": faker.last_name(),
                  "subject": get_subject_random_choice()}
        )

        response = teacher_helper.delete_teacher(response.json()['id'])

        assert response.json()['detail'] == "Teacher deleted", \
            (f"Wrong error text. Actual: '{response.json()['detail']}', "
             f"but expected: 'Teacher deleted'")


class TestGetTeachers:
    pass


class TestGetTeacher:
    pass
