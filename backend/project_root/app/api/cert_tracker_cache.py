from pathlib import Path
from fastapi import FastAPI, Depends

from data_models.course import Course
from data_models.employee import Employee
from data_accessor.course_handler import CourseHandler
from data_accessor.employee_handler import EmployeeHandler
from data_models.employee_certificate import EmployeeCertificate
from data_processor.cert_tracker_service import CertTrackerService
from data_accessor.employee_certificate_handler import EmployeeCertificateHandler

from functools import lru_cache # Dependency factories (load CSVs once via lru_cache)

app = FastAPI(title="Certificate Manager")

@lru_cache()
def get_employee_repo():
    return EmployeeHandler(Path("data/employees.csv"), Employee)

@lru_cache()
def get_course_repo():
    return CourseHandler(Path("data/courses.csv"), Course)

@lru_cache()
def get_employee_cert_repo():
    return EmployeeCertificateHandler(Path("data/employee_certs.csv"), EmployeeCertificate)

@lru_cache()
def get_service(
    emp_cert_repo=Depends(get_employee_cert_repo),
    course_repo=Depends(get_course_repo),
    emp_repo=Depends(get_employee_repo),
):
    return CertTrackerService(emp_cert_repo, course_repo, emp_repo)
