import random

from faker import Faker

from logger.logger import Logger
from services.university.models.base_teacher import SubjectEnum
from services.university.models.teacher_request import TeacherRequest
from services.university.university_service import UniversityService

faker = Faker()


class TestTeacherUpdate:
    def test_update_teacher_first_name(self, university_api_utils_admin):
        Logger.info('### Step 1. Create a teacher')

        university_service = UniversityService(
            api_utils=university_api_utils_admin)

        last_name = faker.last_name()
        subject = random.choice(
            [subj for subj in SubjectEnum])

        teacher = TeacherRequest(first_name=faker.first_name(),
                                 last_name=last_name,
                                 subject=subject)

        create_teacher_response = university_service.create_teacher(
            teacher)

        Logger.info("### Step 2. Update teacher's first name")

        teacher = TeacherRequest(first_name=faker.first_name(),
                                 last_name=last_name,
                                 subject=subject)

        update_teacher_response = university_service.update_teacher(
            teacher_id=create_teacher_response.id,
            teacher_request=teacher)

        assert update_teacher_response.id == create_teacher_response.id, \
            (f"Wrong IDs. Actual: '{update_teacher_response.id}', "
             f"but expected: '{create_teacher_response.id}'")

        assert (update_teacher_response.first_name !=
                create_teacher_response.first_name), \
            (f"Teacher name did not update."
             f"Actual: '{update_teacher_response.first_name}', "
             f"but expected: '{create_teacher_response.first_name}'")
