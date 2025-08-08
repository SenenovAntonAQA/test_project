import pytest
from faker import Faker
from services.university.helpers.group_helper import GroupHelper

faker = Faker()


@pytest.fixture(scope="module")
def created_group(university_api_utils_admin):
    group_helper = GroupHelper(university_api_utils_admin)
    response = group_helper.post_groups(json={
        "name": "test_students" + faker.name()})
    group_id = response.json()["id"]

    yield group_id

    group_helper.delete_group(group_id)
