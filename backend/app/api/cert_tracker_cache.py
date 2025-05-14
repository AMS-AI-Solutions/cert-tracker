from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List
from datetime import date

app = FastAPI(title="Certificate Manager")

# Dependency factories (load CSVs once via lru_cache)
from functools import lru_cache

@lru_cache()
def get_employee_repo():
    return EmployeeRepository(Path("data/employees.csv"), Employee)

@lru_cache()
def get_course_repo():
    return CourseRepository(Path("data/courses.csv"), Course)

@lru_cache()
def get_employee_cert_repo():
    return EmployeeCertificateRepository(Path("data/employee_certs.csv"), EmployeeCertificate)

@lru_cache()
def get_service(
    emp_cert_repo=Depends(get_employee_cert_repo),
    course_repo=Depends(get_course_repo),
    emp_repo=Depends(get_employee_repo),
):
    return CertificateService(emp_cert_repo, course_repo, emp_repo)