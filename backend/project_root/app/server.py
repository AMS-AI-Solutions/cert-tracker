import uvicorn
from fastapi import FastAPI
from app.api.cert_tracker_app import CertTrackerApp

app = CertTrackerApp().app

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )