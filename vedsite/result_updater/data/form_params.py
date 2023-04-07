# coding=utf-8

from ..checking_system.aggregator import *

_params = {
    "qwerty": {
        "blocks": [
            {
                "tasks": {
                    "ДЗ 1": [-1, lambda x: "B2"]
                },
                "system": "yandex.contest",
                "check_type": "automatic",
                "aggregator": UniformWeightedAggregator(),
                "student_name_start_cell": "A2"
            }
        ],
        "mapping_file": "qwerty_students.csv",
        "form_backend": "excel",  # google
        "resource_name": "оценки_qwerty.xlsx"
    }
}


def get_params(course_name):
    try:
        return _params[course_name]
    except:
        raise Exception("Wrong course name!")


def get_course_names():
    return list(_params.keys())
