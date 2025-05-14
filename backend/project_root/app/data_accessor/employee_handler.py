from pathlib import Path
from typing import List, Optional

from data_models.employee import Employee
from data_accessor.csv_handler import CsvHandler

class EmployeeHandler(CsvHandler[Employee]):
    """
    Repository for Employee data loaded from a CSV file.
    """
    def __init__(self, file_path: Path):
        # Initialize with the file path and Employee model
        super().__init__(file_path, Employee)
        # Cache to avoid reloading CSV on each lookup
        self._cache: Optional[List[Employee]] = None

    def load_all(self) -> List[Employee]:
        """Load and cache all employees from CSV."""
        if self._cache is None:
            self._cache = super().load_all()
        return self._cache

    def get_by_id(self, employee_id: int) -> Optional[Employee]:
        """Retrieve an employee by their ID."""
        return next((e for e in self.load_all() if e.employee_id == employee_id), None)