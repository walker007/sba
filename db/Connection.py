from helpers.get_path import get_path
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


Base = declarative_base()


def db_connection():
    return create_engine("sqlite:///" + get_path('assets/database.db'), future=True)


Transaction = Session(db_connection())