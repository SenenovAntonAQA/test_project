import random
import time

import pytest
import requests

from faker import Faker
from services.auth.auth_service import AuthService
from services.auth.models.login_request import LoginRequest
from services.auth.models.register_request import RegisterRequest
from services.university.models.base_student import DegreeEnum
from services.university.models.base_teacher import SubjectEnum
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.models.teacher_request import TeacherRequest
from services.university.university_service import UniversityService
from utils.api_utils import ApiUtils
from utils.random_utils import generate_russian_phone

faker = Faker()


@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_anonym():
    api_utils = ApiUtils(url=AuthService.SERVICE_URL)
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def university_api_utils_anonym():
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL)
    return api_utils

@pytest.fixture(scope="function", autouse=False)
def access_token(auth_api_utils_anonym):
    auth_service = AuthService(auth_api_utils_anonym)
    username = faker.user_name()
    password = faker.password(length=30,
                              special_chars=True,
                              digits=True,
                              upper_case=True,
                              lower_case=True)
    auth_service.register_user(
        register_request=RegisterRequest(username=username,
                                         password=password,
                                         password_repeat=password,
                                         email=faker.email()))
    login_response = auth_service.login_user(
        login_request=LoginRequest(username=username,
                                   password=password))
    return login_response.access_token

@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_admin(access_token):
    api_utils = ApiUtils(url=AuthService.SERVICE_URL, headers={
        "Authorization": f"Bearer {access_token}"})
    return api_utils

@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_invalid_token():
    api_utils = ApiUtils(url=AuthService.SERVICE_URL, headers={
        "Authorization": f"Invalid test token"})
    return api_utils

@pytest.fixture(scope="function", autouse=False)
def university_api_utils_admin(access_token):
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL, headers={
        "Authorization": f"Bearer {access_token}"})
    return api_utils

@pytest.fixture(scope="function", autouse=False)
def university_api_utils_invalid_token():
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL, headers={
        "Authorization": f"Invalid test token"})
    return api_utils

@pytest.fixture(scope="session", autouse=True)
def auth_service_readiness():
    timeout = 180
    start_time = time.time()
    while time.time() < start_time + timeout:
        try:
            response = requests.get(AuthService.SERVICE_URL + "/docs")
            response.raise_for_status()
        except:
            time.sleep(1)
        else:
            break
    else:
        raise RuntimeError(f"Auth service wasn't started during '{timeout}' s.")

@pytest.fixture
def created_group(university_api_utils_admin):
    university_service = UniversityService(api_utils=university_api_utils_admin)
    group = GroupRequest(name=faker.name())
    group_response = university_service.create_group(group_request=group)

    return group_response.id


@pytest.fixture
def created_teacher(university_api_utils_admin):
    university_service = UniversityService(api_utils=university_api_utils_admin)
    teacher = TeacherRequest(first_name=faker.first_name(),
                             last_name=faker.last_name(),
                             subject=random.choice(
                                 [subj for subj in SubjectEnum]))
    teacher_response = university_service.create_teacher(teacher)

    return teacher_response.id

@pytest.fixture
def created_student(university_api_utils_admin, created_group):
    university_service = UniversityService(api_utils=university_api_utils_admin)
    student = StudentRequest(first_name=faker.first_name(),
                             last_name=faker.last_name(),
                             email=faker.email(),
                             degree=random.choice(
                                 [degree for degree in DegreeEnum]),
                             phone=generate_russian_phone(),
                             group_id=created_group)
    student_response = university_service.create_student(student)
    return student_response.id
