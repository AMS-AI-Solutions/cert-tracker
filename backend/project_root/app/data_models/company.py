from pydantic import BaseModel

class Company(BaseModel):
    company_id: int
    company_name: str
    company_email: str
    