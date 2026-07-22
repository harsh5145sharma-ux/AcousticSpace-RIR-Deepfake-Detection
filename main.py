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
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import auth_router, predict, history

# Database tables banao (agar already nahi bane)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AcousticSpace API",
    description="Backend API for Deepfake Detection using Room Impulse Response (RIR).",
    version="1.0.0",
    contact={
        "name": "AcousticSpace Backend Team",
        "email": "backend@acousticspace.local"
    },
    license_info={
        "name": "MIT License"
    }
)

# CORS setup — Member 4 (React frontend) se requests allow karne ke liye
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers include karo
app.include_router(auth_router.router)
app.include_router(predict.router)
app.include_router(history.router)

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "AcousticSpace Backend",
        "version": "1.0.0",
        "message": "Backend service is running successfully"
    }


@app.get("/", tags=["Health"])
def root():
    return {"message": "Welcome to AcousticSpace API. Visit /docs for API documentation."}
