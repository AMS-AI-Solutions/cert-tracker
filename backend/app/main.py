import uvicorn
from fastapi import FastAPI
from app.api.v1.certificates import router as certificates_router

# Create FastAPI app
app = FastAPI(title="Certificate Manager")

# Mount API routers
app.include_router(certificates_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",    # module:path to app instance
        host="0.0.0.0",    # listen on all interfaces
        port=8000,
        reload=True         # auto-reload on code changes (dev only)
    )