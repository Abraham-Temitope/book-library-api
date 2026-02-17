from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./library.db"  # Local SQLite file

engine = create_engine(SQLALCHEMY_DATABASE_URL)  # Connects to DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Session factory
Base = declarative_base()  # Base class for models

def get_db():  # Dependency for DB sessions
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()