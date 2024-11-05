import os.path
from sqlmodel import SQLModel, create_engine, Session

from src.config import DB_NAME

sqlite_url = f"sqlite:///{DB_NAME}"

engine = create_engine(sqlite_url)
session = Session(engine)


def db_setup():
    SQLModel.metadata.create_all(engine)
