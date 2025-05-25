from typing import List
from datetime import date
from fastapi import APIRouter, HTTPException, Query

from app.data_models.employee_certificate import EmployeeCertificate
from app.data_processor.cert_tracker_service import CertTrackerService

class CertTrackerAPI:
    """
    Encapsulates the certificate-related endpoints.
    """
    def __init__(self, service: CertTrackerService):
        self.router = APIRouter()
        self.service = service

        # Register endpoints
        self.router.get(
            "/certificates/expiring",
            response_model=List[EmployeeCertificate],
            tags=["Certificates"]
        )(self.list_expiring)

    def list_expiring(
        self,
        start: date = Query(..., description="Start of date range"),
        end: date = Query(..., description="End of date range"),
    ) -> List[EmployeeCertificate]:
        """
        List certificates expiring between start and end dates.
        """
        if start > end:
            raise HTTPException(status_code=400, detail="start must be before end")
        return self.service.get_expiring_certificates(start, end)