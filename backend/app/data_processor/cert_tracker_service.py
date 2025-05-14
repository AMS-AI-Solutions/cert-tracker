from datetime import date

class CertificateService:
    def __init__(
        self,
        employee_cert_repo: EmployeeCertificateRepository,
        course_repo: CourseRepository,
        employee_repo: EmployeeRepository,
    ):
        self.employee_certs = employee_cert_repo.load_all()
        self.courses = {c.course_id: c for c in course_repo.load_all()}
        self.employees = {e.employee_id: e for e in employee_repo.load_all()}

    def get_expiring_certificates(
        self, start: date, end: date
    ) -> List[EmployeeCertificate]:
        return [cert for cert in self.employee_certs
                if start <= cert.expiry_date <= end]