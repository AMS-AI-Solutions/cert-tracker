# app/api/v1/certificates.py
from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query

# Import Pydantic model and service factory
from data_models.employee_certificate import EmployeeCertificate
from api.cert_tracker_cache import get_service

# Define the router
router = APIRouter()

@router.get(
    "/certificates/expiring",
    response_model=List[EmployeeCertificate],
    tags=["Certificates"]
)

def list_expiring(
    start: date = Query(..., description="Start of date range"),
    end: date = Query(..., description="End of date range"),
    service = Depends(get_service)
) -> List[EmployeeCertificate]:
    """List certificates expiring between start and end dates."""
    if start > end:
        raise HTTPException(status_code=400, detail="start must be before end")
    return service.get_expiring_certificates(start, end)