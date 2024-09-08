from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from src.settings.settings import DATABASE_SETTINGS

# creating the engine
engine = create_engine(url=DATABASE_SETTINGS["URL"])

# creating the db session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declare a mapping Base class
Base = declarative_base()

db = scoped_session(SessionLocal)


# Dependency to get the database session
def get_db():
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()
