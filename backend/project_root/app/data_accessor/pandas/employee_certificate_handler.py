from pathlib import Path
from datetime import date, timedelta
from collections import Counter, defaultdict
from typing import Dict, List, Optional

from app.data_models.employee_certificate import EmployeeCertificate
from app.data_accessor.pandas.pandas_handler import PandasHandler
from app.data_accessor.interfaces.employee_certificate_handler_interface import (
    EmployeeCertificateHandlerInterface,
)

CertList = List[EmployeeCertificate]
IntMap = Dict[int, int]
StrMap = Dict[str, int]


class EmployeeCertificateHandler(
    PandasHandler[EmployeeCertificate],
    EmployeeCertificateHandlerInterface,
):
    """
    Query and cache EmployeeCertificate records in a Pandas DataFrame.
    """

    def __init__(self, file_path: Path):
        super().__init__(
            file_path=file_path,
            model=EmployeeCertificate,
            parse_dates=["issue_date", "expiry_date"],
            index_col=None,
        )
        # Convert pandas Timestamp → date for comparisons
        for col in ("issue_date", "expiry_date"):
            self.df[col] = self.df[col].dt.date

    def get_by_id(self, certificate_id: str) -> Optional[EmployeeCertificate]:
        """
        Retrieve a certificate by its unique ID.
        (Implementing abstract method from the interface.)
        """
        return self.get_certificate_by_id(certificate_id)

    def get_certificate_by_id(self, certificate_id: str) -> Optional[EmployeeCertificate]:
        """
        Retrieve a certificate by its unique ID.
        """
        return next(
            (
                cert
                for cert in self.load_all()
                if str(cert.certificate_id) == str(certificate_id)
            ),
            None,
        )

    def find_by_certificate_name(self, search_term: str) -> CertList:
        """
        Return all certificates whose `certificate_name` contains the given search term,
        matching case-insensitively.
        """
        term = search_term.lower()
        return [
            cert
            for cert in self.load_all()
            if term in cert.certificate_name.lower()
        ]

    def count_certificates_by_employee(self) -> IntMap:
        """
        Map employee_id → number of certificates held.
        """
        return dict(Counter(cert.employee_id for cert in self.load_all()))

    def count_certificates_by_course(self) -> StrMap:
        """
        Map course_id → number of certificates issued.
        """
        return dict(Counter(cert.course_id for cert in self.load_all()))

    def group_certificates_by_employee(self) -> Dict[int, CertList]:
        """
        Map employee_id → list of that employee's certificates.
        """
        groups: Dict[int, CertList] = defaultdict(list)
        for cert in self.load_all():
            groups[cert.employee_id].append(cert)
        return dict(groups)

    def group_certificates_by_course(self) -> Dict[str, CertList]:
        """
        Map course_id → list of certificates for that course.
        """
        groups: Dict[str, CertList] = defaultdict(list)
        for cert in self.load_all():
            groups[cert.course_id].append(cert)
        return dict(groups)

    def get_employee_certificates_by_employee_id(self, employee_id: int) -> CertList:
        """
        Retrieve all certificates for a specific employee.
        """
        return [
            cert
            for cert in self.load_all()
            if cert.employee_id == employee_id
        ]

    def get_employee_certificates_by_course_id(self, course_id: str) -> CertList:
        """
        Retrieve all certificates for a specific course.
        """
        return [
            cert
            for cert in self.load_all()
            if cert.course_id == course_id
        ]

    def get_certificates_expiring_in_time_range(
        self, start_date: date, end_date: date
    ) -> CertList:
        """
        Retrieve certificates with expiry dates between start_date and end_date, inclusive.
        """
        return [
            cert
            for cert in self.load_all()
            if start_date <= cert.expiry_date <= end_date
        ]

    def get_certificates_expiring_within(
        self, days: int, from_date: date
    ) -> CertList:
        """
        Retrieve certificates whose expiry_date falls between `from_date`
        and `from_date + days`, inclusive.
        """
        cutoff = from_date + timedelta(days=days)
        return self.get_certificates_expiring_in_time_range(from_date, cutoff)

    def get_upcoming_expirations(self, days_ahead: int) -> CertList:
        """
        Get certificates expiring within the next `days_ahead` days from today.
        """
        today = date.today()
        return self.get_certificates_expiring_in_time_range(
            today, today + timedelta(days=days_ahead)
        )

    def count_expirations_by_company(self, days_ahead: int) -> Dict[str, int]:
        """
        Count upcoming expirations, grouped by sponsoring company.
        """
        upcoming = self.get_upcoming_expirations(days_ahead)
        return dict(Counter(cert.sponsoring_company for cert in upcoming))  # type: ignore

    def certificates_by_employee_summary(self) -> Dict[int, List[str]]:
        """
        Map each employee_id → list of their certificate names.
        """
        summary: Dict[int, List[str]] = defaultdict(list)
        for cert in self.load_all():
            summary[cert.employee_id].append(cert.certificate_name)
        return dict(summary)
