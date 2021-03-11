import os
import csv
from pathlib import Path

from typing import TypedDict, List


class Employee(TypedDict):
    name: str
    location: str


class Employees(object):
    def __init__(self, employees: List[Employee]):
        self.employees = employees

    employees: List[Employee]


def csv_to_employees(path: str) -> Employees:
    employees = []
    with open(Path(path).absolute().as_posix()) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=["name", "location"])
        for employee in reader:
            employees.append(employee)
    return Employees(employees)
