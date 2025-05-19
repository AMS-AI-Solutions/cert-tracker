from app.data_accessor.csv_handler import CsvHandler
from app.data_models.employee_certificate import EmployeeCertificate
from pathlib import Path
from typing import List, Optional
from datetime import date

class EmployeeCertificateHandler(CsvHandler[EmployeeCertificate]):
    """
    Handler for Employee Certificate data loaded from a CSV file.
    """
    def __init__(self, file_path: Path):
        super().__init__(file_path, EmployeeCertificate)
        self._cache: Optional[List[EmployeeCertificate]] = None

    def load_all(self) -> List[EmployeeCertificate]:
        """Load and cache all employee certificates from CSV."""
        if self._cache is None:
            self._cache = super().load_all()
        return self._cache

    def get_employee_certificates_by_employee_id(self, employee_id: int) -> List[EmployeeCertificate]:
        """Retrieve all certificates for a specific employee by their ID."""
        return [cert for cert in self.load_all() if cert.employee_id == employee_id]

    def get_expired_employee_certificates_by_date_range(self, start_date: date, end_date: date) -> List[EmployeeCertificate]:
        """Retrieve all expired employee certificates within a specific date range."""
        return [
            cert for cert in self.load_all()
            if start_date <= cert.expiry_date and cert.expiry_date <= end_date
        ]

    def get_employee_certificates_by_course_id(self, course_id: int) -> List[EmployeeCertificate]:
        """Retrieve all certificates for a specific course by its ID."""
        return [cert for cert in self.load_all() if cert.course_id == course_id]
