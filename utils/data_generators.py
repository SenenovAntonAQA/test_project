import random

from faker import Faker

from services.university.models.base_student import DegreeEnum
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.university_service import UniversityService
from utils.random_utils import generate_russian_phone

faker = Faker()


def generate_groups_and_students(api_utils, students, groups):
    """Создаем в группах 'groups' студентов 'students' и возвращаем кортеж"""
    student_ids = {}

    university_service = UniversityService(
        api_utils=api_utils)

    for i in range(groups):
        group_response = university_service.create_group(
            GroupRequest(name="test_grades" + faker.name()))
        for j in range(students):
            student_response = university_service.create_student(StudentRequest(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                degree=random.choice(
                    [degree for degree in DegreeEnum]),
                phone=generate_russian_phone(),
                group_id=group_response.id))
            if group_response.id not in student_ids:
                student_ids[group_response.id] = [student_response.id]
            else:
                student_ids[group_response.id].append(student_response.id)

    return student_ids
