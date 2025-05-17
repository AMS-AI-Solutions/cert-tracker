from pathlib import Path
from typing import List, Optional

from app.data_models.employee import Employee
from app.data_accessor.csv_handler import CsvHandler

class EmployeeHandler(CsvHandler[Employee]):
    """
    Handler for Employee data loaded from a CSV file.
    """
    def __init__(self, file_path: Path):
        super().__init__(file_path, Employee)
        self._cache: Optional[List[Employee]] = None

    def load_all(self) -> List[Employee]:
        """Load and cache all employees from CSV."""
        if self._cache is None:
            self._cache = super().load_all()
        return self._cache

    def get_by_id(self, employee_id: int) -> Optional[Employee]:
        """Retrieve an employee by their ID."""
        return next((e for e in self.load_all() if e.employee_id == employee_id), None)
    
    def get_employee_company_name(self, first_name: str, last_name: str) -> Optional[str]:
        """Retreive name of a company associated to an employee"""
        return next((e.company_name for e in self.load_all() if e.first_name == first_name and e.last_name == last_name), None)
    
    def get_employee_email(self, first_name: str, last_name: str) -> Optional[str]:
        """Retreive the email of an employee"""
        return next((e.email for e in self.load_all() if e.first_name == first_name and e.last_name == last_name), None)