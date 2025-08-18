import random

from faker import Faker

from constants.constants import GradeConstants

faker = Faker()


def generate_unique_group_id(existing_numbers: list, min=1, max=1000):
    available_numbers = list(set(range(min, max + 1)) - set(existing_numbers))
    if not available_numbers:
        raise ValueError("No available group numbers left to choose from.")
    return random.choice(available_numbers)


def generate_invalid_group_ids():
    return [-random.randint(1, 100),
            0,
            random.randint(1000, 1000000)]


def generate_invalid_groups():
    return [-random.randint(1, 100),
            0,
            None,  # null
            " ",
            ""]


def generate_invalid_names():
    symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=',
               '-', '[', ']', '{', '}', ';', ':', ',', '.', '/', '<', '>', '?']
    return [random.randint(1, 100),  # int
            True,  # bool
            None,  # null
            {},  # dict
            [],  # list
            " ",
            "",
            random.choice(symbols)
            ]


def generate_invalid_email():
    return [random.randint(1, 100),  # int
            True,  # bool
            None,  # null
            [],  # list
            " ",
            "",
            "test",
            "test@",
            "test@yandex",
            "@yandex.ru"]


def get_grade_random_choice():
    """Возвращаем оценку в диапазоне [MIN_GRADE, MAX_GRADE]."""
    return random.randint(GradeConstants.MIN_GRADE, GradeConstants.MAX_GRADE)


def get_subject_random_choice():
    return random.choice(
        ['Mathematics',
         'Physics',
         'History',
         'Biology',
         'Geography'])


def get_degree_random_choice():
    return random.choice(
        ['Associate',
         'Bachelor',
         'Master',
         'Doctorate'])


def generate_russian_phone():
    city_prefixes = [str(i) for i in range(800, 900)]
    mobile_prefixes = [str(i) for i in range(900, 1000)]

    prefix = random.choice(city_prefixes + mobile_prefixes)
    return faker.numerify(f"+7{prefix}#######")
