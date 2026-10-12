from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# Resolve relative to this module, never the shell's working directory.
from pathlib import Path
import os

DATABASE_PATH = Path(__file__).resolve().parents[2] / "recovery_tracker.db"
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DATABASE_PATH}")



engine = create_engine( #this is the connection to the database
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker( #a session is how your application interacts with the database, how we create database sessions
    autocommit=False,
    autoflush=False,
    bind=engine
)


class Base(DeclarativeBase): #every sql alchemy database model we create will inherit from Base
    pass