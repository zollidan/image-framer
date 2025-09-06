# database.py
"""
Database configuration and session management for the application.

This module sets up the SQLAlchemy engine and session management for the SQLite database.
It provides a dependency `get_db` to get a database session.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency to get a database session.

    This function is a generator that yields a new database session
    for each request and ensures that the session is closed afterward.

    Yields:
        Session: A new SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
