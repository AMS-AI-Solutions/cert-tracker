from pathlib import Path
from typing import List, Optional, Dict
from datetime import date, timedelta
from collections import Counter, defaultdict

from app.data_accessor.csv_handler import CsvHandler
from app.data_models.employee_certificate import EmployeeCertificate

class EmployeeCertificateHandler(CsvHandler[EmployeeCertificate]):
    """
    Handler for Employee Certificate data loaded from a CSV file.
    Provides both read-only querying and cache management.
    """
    def __init__(self, file_path: Path):
        super().__init__(file_path, EmployeeCertificate)
        self._cache: Optional[List[EmployeeCertificate]] = None

    def load_all(self) -> List[EmployeeCertificate]:
        """Load and cache all employee certificates from CSV."""
        if self._cache is None:
            self._cache = super().load_all()
        return self._cache

    def reload_all(self) -> None:
        """Clear cache to force reloading from CSV on next access."""
        self._cache = None

    # Alias for reload_all
    clear_cache = reload_all

    def get_certificate_by_id(self, certificate_id: str) -> Optional[EmployeeCertificate]:
        """Retrieve a single certificate by its unique ID."""
        return next(
            (cert for cert in self.load_all() if cert.certificate_id == certificate_id),
            None
        )

    def get_employee_certificates_by_employee_id(self, employee_id: int) -> List[EmployeeCertificate]:
        """Retrieve all certificates for a specific employee by their ID."""
        return [cert for cert in self.load_all() if cert.employee_id == employee_id]

    def get_employee_certificates_by_course_id(self, course_id: str) -> List[EmployeeCertificate]:
        """Retrieve all certificates for a specific course by its ID."""
        return [cert for cert in self.load_all() if cert.course_id == course_id]

    def get_expired_employee_certificates_by_date_range(
        self, start_date: date, end_date: date
    ) -> List[EmployeeCertificate]:
        """Retrieve all expired employee certificates within a specific date range."""
        return [
            cert for cert in self.load_all()
            if start_date <= cert.expiry_date <= end_date
        ]

    def get_active_certificates(self, as_of: date = date.today()) -> List[EmployeeCertificate]:
        """Retrieve all certificates not yet expired as of a given date."""
        return [cert for cert in self.load_all() if cert.expiry_date > as_of]

    def get_expired_certificates(self, as_of: date = date.today()) -> List[EmployeeCertificate]:
        """Retrieve all certificates already expired as of a given date."""
        return [cert for cert in self.load_all() if cert.expiry_date <= as_of]

    def get_certificates_expiring_within(
        self, days: int, from_date: date = date.today()
    ) -> List[EmployeeCertificate]:
        """Retrieve certificates expiring within the next N days."""
        cutoff = from_date + timedelta(days=days)
        return [
            cert for cert in self.load_all()
            if from_date <= cert.expiry_date <= cutoff
        ]

    def count_certificates_by_employee(self) -> Dict[int, int]:
        """Count how many certificates each employee holds."""
        return Counter(cert.employee_id for cert in self.load_all())

    def count_certificates_by_course(self) -> Dict[str, int]:
        """Count how many certificates have been issued per course."""
        return Counter(cert.course_id for cert in self.load_all())

    def group_certificates_by_employee(self) -> Dict[int, List[EmployeeCertificate]]:
        """Group certificates into lists keyed by employee ID."""
        groups: Dict[int, List[EmployeeCertificate]] = defaultdict(list)
        for cert in self.load_all():
            groups[cert.employee_id].append(cert)
        return groups

    def group_certificates_by_course(self) -> Dict[str, List[EmployeeCertificate]]:
        """Group certificates into lists keyed by course ID."""
        groups: Dict[str, List[EmployeeCertificate]] = defaultdict(list)
        for cert in self.load_all():
            groups[cert.course_id].append(cert)
        return groups

    def find_by_certificate_name(self, substr: str) -> List[EmployeeCertificate]:
        """Case-insensitive substring search on certificate_name."""
        term = substr.lower()
        return [
            cert for cert in self.load_all()
            if term in cert.certificate_name.lower()
        ]