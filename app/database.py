from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from .config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}, 
    pool_size=10,
    max_overflow=2,
    pool_recycle=180,  
    pool_pre_ping=True
    
)

SessionLocal = sessionmaker(
    bind = engine,
    autoflush=False,
    autocommit = False
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
