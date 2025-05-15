from pydantic import BaseModel

class Company(BaseModel):
    company_id: str
    company_name: str
    company_email: str
    