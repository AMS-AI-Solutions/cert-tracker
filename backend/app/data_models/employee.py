from pydantic import BaseModel, EmailStr
from datetime import date

class Employee(BaseModel):
    employee_id: int
    first_name: str
    last_name: str
    department: str
    hire_date: date
    email: EmailStr