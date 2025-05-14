from typing import List
from datetime import date
from fastapi import Depends, HTTPException, Query

from cert_tracker_cache import get_service
from data_models.employee_certificate import EmployeeCertificate
from data_processor.cert_tracker_service import CertTrackerService

@app.get("/certificates/expiring", response_model=List[EmployeeCertificate])

def list_expiring(
    start: date = Query(..., description="Start of date range"),
    end: date = Query(..., description="End of date range"),
    service: CertTrackerService = Depends(get_service),
):
    if start > end:
        raise HTTPException(status_code=400, detail="start must be before end")
    return service.get_expiring_certificates(start, end)