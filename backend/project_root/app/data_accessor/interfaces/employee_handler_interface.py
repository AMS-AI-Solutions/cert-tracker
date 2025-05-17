from abc import ABC, abstractmethod
from typing import List, Optional
from app.data_models.employee import Employee

class EmployeeHandlerInterface(ABC):
    @abstractmethod
    def load_all(self) -> List[Employee]: ...
    
    @abstractmethod
    def get_by_id(self, employee_id: int) -> Optional[Employee]: ...

    @abstractmethod
    def get_company_name_from_employee_name(self, employee_name: str) -> Optional[str]: ...