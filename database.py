from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL ="postgresql://postgres:vipul@localhost:5432/pizza_api_db"

engine = create_engine(DATABASE_URL,echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

if not database_exists(DATABASE_URL):
    create_database(DATABASE_URL)


