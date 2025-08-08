import random

import pytest
import requests.status_codes
from faker import Faker

from services.university.helpers.group_helper import GroupHelper
from utils.random_utils import generate_invalid_group_ids, \
    generate_invalid_names

faker = Faker()


class TestGroupContract:
    def test_create_group_anonym(self, university_api_utils_anonym):
        group_helper = GroupHelper(api_utils=university_api_utils_anonym)
        response = group_helper.post_groups(json={"name": faker.name()})

        assert (response.status_code ==
                requests.status_codes.codes.unauthorized), \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.unauthorized}'")

    def test_create_new_group(self, university_api_utils_admin):
        group_helper = GroupHelper(university_api_utils_admin)
        group_name = faker.name()
        response = group_helper.post_groups(json={"name": group_name})

        assert (response.status_code ==
                requests.status_codes.codes.created), \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.created}'")

        response = group_helper.get_groups()
        groups = response.json()
        group_names = [group["name"] for group in groups]

        assert group_name in group_names, \
            (f"Group name '{group_name}' not found in groups: "
             f"'{group_names}'")

    @pytest.mark.parametrize("group_name", generate_invalid_names())
    def test_create_group_invalid_name_type(self, university_api_utils_admin,
                                            group_name):
        group_helper = GroupHelper(university_api_utils_admin)
        response = group_helper.post_groups(json={"name": group_name})

        assert (response.status_code ==
                requests.status_codes.codes.unprocessable), \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.unprocessable}'")

    def test_delete_group(self, university_api_utils_admin):
        group_helper = GroupHelper(university_api_utils_admin)
        response = group_helper.post_groups(json={"name": faker.name()})
        group_id = response.json().get("id")
        response = group_helper.delete_group(str(group_id))

        assert (response.status_code ==
                requests.status_codes.codes.ok), \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.ok}'")

        response = group_helper.get_groups()
        groups = response.json()
        group_ids = [group["id"] for group in groups]

        assert group_id not in group_ids, \
            (f"Group with id '{group_id}' is still present in: "
             f"'{groups}'")

    @pytest.mark.parametrize("group_id", generate_invalid_group_ids())
    def test_get_nonexistent_group(self, university_api_utils_admin, group_id):
        group_helper = GroupHelper(university_api_utils_admin)
        response = group_helper.get_group(str(group_id))

        assert (response.status_code ==
                requests.status_codes.codes.not_found), \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.not_found}'")

    def test_wrong_group_rename(self, university_api_utils_admin):
        group_helper = GroupHelper(university_api_utils_admin)
        response = group_helper.get_groups()
        groups = response.json()
        group_names = [group["name"] for group in groups]

        response = group_helper.post_groups(json={"name": faker.name()})
        group_id = response.json().get("id")

        response = group_helper.update_group(
            group_id=str(group_id), json={"name": random.choice(group_names)})

        assert (response.status_code ==
                requests.status_codes.codes.conflict), \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.conflict}'")
