from pydantic import BaseModel, EmailStr
from datetime import date

class EmployeeCertificate(BaseModel):
    employee_id: int
    course_id: str
    certificate_name: str
    issue_date: date
    expiry_date: date