import random

from faker import Faker

faker = Faker()

def generate_unique_group_id(existing_numbers: list, min = 1, max = 1000):
    available_numbers = list(set(range(min, max+1)) - set(existing_numbers))
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
    return random.randint(1, 5)

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
    prefix = random.choice(
        ['901', '902', '903', '904', '905', '906', '908', '909',
         '910', '911', '912', '913', '914', '915', '916', '917',
         '918', '919', '920', '921', '922', '923', '924', '925',
         '926', '927', '928', '929', '930', '931', '932', '933',
         '934', '936', '937', '938', '939', '950', '951', '952',
         '953', '954', '955', '956', '957', '958', '959', '960',
         '961', '962', '963', '964', '965', '966', '967', '968',
         '969', '970', '971', '977', '978', '980', '981', '982',
         '983', '984', '985', '986', '987', '988', '989', '991',
         '992', '993', '994', '995', '996', '997', '998', '999'])
    return faker.numerify(f"+7{prefix}#######")
