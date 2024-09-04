from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable not found.")
    raise ValueError("DATABASE_URL environment variable has to be set.")

engine = create_engine(
    DATABASE_URL,
    pool_size=10,     
    max_overflow=20,  
    pool_timeout=30,  
    pool_recycle=1800,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Session rollback due to exception: {e}")
        db.rollback()
        raise
    finally:
        db.close()
        logger.info("Database session closed.")
