@app.get("/certificates/expiring", response_model=List[EmployeeCertificate])

def list_expiring(
    start: date = Query(..., description="Start of date range"),
    end: date = Query(..., description="End of date range"),
    service: CertificateService = Depends(get_service),
):
    if start > end:
        raise HTTPException(status_code=400, detail="start must be before end")
    return service.get_expiring_certificates(start, end)