"""
Database connection setup.
SQLite for development — production mein isko PostgreSQL se replace karna
(bas SQLALCHEMY_DATABASE_URL change karna hoga).
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./acousticspace.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency — har request ke liye ek DB session deta hai."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
