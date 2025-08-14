import random

from faker import Faker

from logger.logger import Logger
from services.university.models.base_teacher import SubjectEnum
from services.university.models.teacher_request import TeacherRequest
from services.university.university_service import UniversityService

faker = Faker()


class TestTeacherCreate:
    def test_create_and_check_teacher(self, university_api_utils_admin):
        Logger.info('### Step 1. Create teacher')
        university_service = UniversityService(
            api_utils=university_api_utils_admin)
        subject = random.choice([subj for subj in SubjectEnum])

        teacher = TeacherRequest(first_name=faker.first_name(),
                                 last_name=faker.last_name(),
                                 subject=subject)
        create_teacher_response = university_service.create_teacher(
            teacher)

        Logger.info('### Step 2. Checking the created user in system')
        get_teacher_response = university_service.teacher_info(
            teacher_id=create_teacher_response.id)

        assert get_teacher_response.subject == subject, \
            (f"Wrong teacher subject. Actual: "
             f"{get_teacher_response.subject}', but expected: '{subject}'")

    def test_create_same_teacher(self, university_api_utils_admin):
        Logger.info('### Step 1. Create teacher')
        university_service = UniversityService(
            api_utils=university_api_utils_admin)
        first_name = faker.first_name()
        last_name = faker.last_name()
        subject = random.choice([subj for subj in SubjectEnum])

        teacher = TeacherRequest(first_name=first_name,
                                 last_name=last_name,
                                 subject=subject)
        create_first_teacher_response = university_service.create_teacher(
            teacher)

        Logger.info('### Step 2. Create same teacher')
        create_second_teacher_response = university_service.create_teacher(
            teacher)

        assert (create_first_teacher_response.id !=
                create_second_teacher_response.id), (
            f"Same id: '{create_first_teacher_response.id}'"
            f" when should be different on re-creation")
