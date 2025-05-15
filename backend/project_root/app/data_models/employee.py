from pydantic import BaseModel, EmailStr

class Employee(BaseModel):
    employee_id: int
    first_name: str
    last_name: str
    company_name: str
    department: str
    email: EmailStr