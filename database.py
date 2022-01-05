import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

user_bd = os.getenv("USER_DATABASE")
pass_bd = os.getenv("PASSWORD_DATABASE")
host_db = os.getenv("HOST_DATABASE")
name_bd = os.getenv("NAME_DATABASE")


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{user_bd}:{pass_bd}@{host_db}/{name_bd}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()