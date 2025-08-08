import random

from faker import Faker

from services.auth.helpers.authentication_helper import AuthenticationHelper
from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.student_helper import StudentHelper
from services.auth.helpers.user_helper import UserHelper
from utils.api_utils import ApiUtils

AUTH_URL = "http://127.0.0.1:8000/"
UNIVERSITY_URL = "http://127.0.0.1:8001"

REGISTER_ENDPOINT = "/auth/register/"
LOGIN_ENDPOINT = "/auth/login/"
ME_ENDPOINT = "/users/me/"

GROUPS_ENDPOINT = "/groups/"
STUDENTS_ENDPOINT = "/students/"

faker = Faker()

username = faker.user_name()
password = faker.password() + '".,/;:<=>?`{|}[]'

authentication_helper = AuthenticationHelper(api_utils=ApiUtils(AUTH_URL))

response1 = authentication_helper.post_register(
    data={"username": username,
          "password": password,
          "password_repeat": password,
          "email": faker.email()})

response2 = authentication_helper.post_login(
    data={"username": username,
          "password": password})

access_token = response2.json()["access_token"]
token_type = response2.json()["token_type"]

authentication_admin_helper = UserHelper(api_utils=ApiUtils(
    AUTH_URL, headers={"Authorization": f"{token_type} {access_token}"}))

response3 = authentication_admin_helper.get_me()

admin_university_api_utils = ApiUtils(
    UNIVERSITY_URL,
    headers={"Authorization": f"{token_type} {access_token}"}
)
group_admin_helper = GroupHelper(api_utils=admin_university_api_utils)
student_admin_helper = StudentHelper(api_utils=admin_university_api_utils)

response4 = group_admin_helper.post_groups(json={"name": faker.name()})

response5 = student_admin_helper.post_students(
    json={"first_name": faker.first_name(),
          "last_name": faker.last_name(),
          "email": faker.email(),
          "degree": random.choice(
              ['Associate',
               'Bachelor',
               'Master',
               'Doctorate']),
          "phone": faker.numerify(
              "+7##########"),
          "group_id": response4.json()['id']})
