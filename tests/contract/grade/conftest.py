import pytest
from faker import Faker
from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.teacher_helper import TeacherHelper
from utils.random_utils import get_subject_random_choice

faker = Faker()


@pytest.fixture(scope="function")
def created_group(university_api_utils_admin):
    group_helper = GroupHelper(university_api_utils_admin)
    response = group_helper.post_groups(json={
        "name": "test_grades" + faker.name()})
    group_id = response.json()["id"]

    return group_id


@pytest.fixture
def created_teacher(university_api_utils_admin):
    teacher_helper = TeacherHelper(university_api_utils_admin)
    response = teacher_helper.post_teachers(
        json={"first_name": faker.first_name(),
               "last_name": faker.last_name(),
               "subject": get_subject_random_choice()})
    teacher_id = response.json()["id"]

    return teacher_id
