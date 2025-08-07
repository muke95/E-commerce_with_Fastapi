
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from core.config import settings  # Must be defined with db_username, db_password, etc.
# DATABASE_URL =  "mysql+mysqlconnector://mukesh:Mukesh%4095@127.0.0.1:3306/ecom"
DATABASE_URL =  f"mysql+mysqlconnector://{settings.db_username}:{settings.db_password}@127.0.0.1:3306/ecom"
# MySQL connection URL using PyMySQL
# DATABASE_URL = f"mysql+pymysql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"

# Create the engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get a DB session (used in FastAPI or other apps)
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# # Run this only manually or from a separate script
# if __name__ == "__main__":
#     from db import models  # Ensure all models are imported
#     Base.metadata.create_all(bind=engine)
#     print("✅ Tables created.")
