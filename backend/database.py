import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from models import Base

load_dotenv()

DEFAULT_DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/ai_crm_hcp"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def build_engine(database_url: str):
    try:
        engine = create_engine(database_url, echo=False)
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return engine
    except Exception:
        fallback_url = "sqlite:///./ai_crm_hcp.db"
        return create_engine(fallback_url, echo=False)


engine = build_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
