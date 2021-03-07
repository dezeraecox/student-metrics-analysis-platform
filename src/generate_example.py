import os, re
import pandas as pd
import numpy as np
import names

from random import randint, sample
from loguru import logger
from GEN_Utils import FileHandling

logger.info('Import OK')

output_folder = 'utilities/'

if not os.path.exists(output_folder):
    os.mkdir(output_folder)


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def grades_dict(num_students, num_tasks):
    return {
        f'Task {x+1} total / 100': [
            randint(0, 100) for i in range(num_students)
        ]
        for x in range(num_tasks)
    }

def wellbeing_dict(num_students, num_terms, subject):
    return {
        incident_type: [
            randint(0, 20) for i in range(num_students * num_terms)
        ]
        for incident_type in [
            'Whole School',
            f'Positives {subject}',
            f'Negatives {subject}',
        ]
    }


example_data = {}

# Prepare master students list
males = [names.get_full_name(gender='male') for x in range(200)]
females = [names.get_full_name(gender='female') for x in range(300)]
student_ids = [random_with_N_digits(7) for x in range(500)]

students = dict(zip(student_ids, males + females))

# Prepare Grades examples
for year in ['2017', '2018', '2019', '2020']:
    sheet_name = f'Grades {year}'
    students_sample = sample(student_ids, 450)
    sheet = {
        'Student Id': students_sample,
        'First Name': [students[student_id].split(' ')[0] for student_id in students_sample],
        'Surname': [students[student_id].split(' ')[1] for student_id in students_sample],
        }
    sheet.update(grades_dict(num_students=450, num_tasks=4))
    sheet = pd.DataFrame(sheet)
    example_data[sheet_name] = sheet


# Prepare Wellbeing examples
for year in ['2017', '2018', '2019', '2020']:
    sheet_name = f'Wellbeing {year}'
    num_terms = 4
    students_sample = sample(student_ids, 450)
    sheet = {
        'Student Id': students_sample * num_terms,
        'First Name': [students[student_id].split(' ')[0] for student_id in students_sample] * num_terms,
        'Surname': [students[student_id].split(' ')[1] for student_id in students_sample] * num_terms,
        'Term' : [item for sublist in [[str(x+1)] * 450 for x in range(4)] for item in sublist]
        }
    sheet.update(wellbeing_dict(num_students=450, num_terms=4, subject='English'))
    sheet = pd.DataFrame(sheet)
    example_data[sheet_name] = sheet

# Prepare Student info example
student_info = []
for sheet, df in example_data.items():
    student_info.append(df[['Student Id', 'First Name', 'Surname']])
student_info = pd.concat(student_info).drop_duplicates()
student_info['Gender'] = ['M' if ' '.join([student[0], student[1]]) in males else 'F' for student in student_info[['First Name', 'Surname']].values]
example_data['Student Info'] = student_info

# Prepare Students to Track example
example_data['Students to Track'] = student_info.sample(25)

# Save to excel
FileHandling.df_to_excel(
    output_path=f'{output_folder}example_data.xlsx',
    sheetnames=list(example_data.keys()),
    data_frames=list(example_data.values())
)