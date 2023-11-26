# -*- coding: utf-8 -*-
from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker


CONNECTION_STRING = getenv('CONNECTION_STRING')


Base = declarative_base()


def create_session() -> Session:
    engine = create_engine(CONNECTION_STRING)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return session()
