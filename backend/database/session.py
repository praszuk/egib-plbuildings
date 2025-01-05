from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.core.config import settings


_SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=create_engine(settings.DATABASE_URL)
)


def get_db():
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()
