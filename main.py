"""
AcousticSpace Backend — Main Entry Point
------------------------------------------
FastAPI application jo audio deepfake detection model ko serve karta hai.

Run karne ke liye:
    uvicorn main:app --reload

Swagger docs yahan milenge:
    http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware,
)

from database import (
    engine,
    Base,
)

from routers import (
    auth_router,
    predict,
    history,
)

from services.ml_service import (
    integration_status,
)


# ----------------------------------------
# Database
# ----------------------------------------

Base.metadata.create_all(
    bind=engine
)


# ----------------------------------------
# FastAPI
# ----------------------------------------

app = FastAPI(
    title="AcousticSpace API",
    description=(
        "Backend API for RIR-based "
        "audio deepfake detection."
    ),
    version="1.0.0",
)


# ----------------------------------------
# CORS
# ----------------------------------------

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ----------------------------------------
# Routers
# ----------------------------------------

app.include_router(
    auth_router.router
)

app.include_router(
    predict.router
)

app.include_router(
    history.router
)


# ----------------------------------------
# Root
# ----------------------------------------

@app.get("/")
def root():

    return {
        "project": "AcousticSpace",
        "backend": "running",
        "version": "1.0.0",
        "docs": "/docs",
    }


# ----------------------------------------
# Health
# ----------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "AcousticSpace Backend",
        "version": "1.0.0",
    }


# ----------------------------------------
# Integration status
# ----------------------------------------

@app.get("/integration-status")
def ml_status():

    return integration_status()