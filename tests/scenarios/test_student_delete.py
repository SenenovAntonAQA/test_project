import random

from faker import Faker

from logger.logger import Logger
from services.university.models.base_student import DegreeEnum
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.university_service import UniversityService
from utils.random_utils import generate_russian_phone

faker = Faker()


class TestStudentDelete:
    def test_delete_student(self, university_api_utils_admin):
        Logger.info('### Step 1. Create group')
        university_service = UniversityService(
            api_utils=university_api_utils_admin)
        group = GroupRequest(name=faker.name())
        group_response = university_service.create_group(group_request=group)

        Logger.info('### Step 2. Create student')
        student = StudentRequest(first_name=faker.first_name(),
                                 last_name=faker.last_name(),
                                 email=faker.email(),
                                 degree=random.choice(
                                     [option for option in DegreeEnum]),
                                 phone=generate_russian_phone(),
                                 group_id=group_response.id)
        create_student_response = university_service.create_student(
            student_request=student)

        Logger.info('### Step 3. Delete student')

        delete_student_response = university_service.delete_student(
            student_id=create_student_response.id)

        assert delete_student_response.detail == "Student deleted", \
            (f"Incorrect details, actual: '{delete_student_response.detail}'"
             f", but expected: 'Student deleted'")
