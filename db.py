from sqlalchemy import create_engine, Integer, String, Column, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('sqlite:///sqlite3.db', echo=True)
base = declarative_base()


class Users(base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    tg_id = Column(Integer(), nullable=False)
    tg_username = Column(String(), nullable=False)
    neck_size = Column(Integer(), nullable=False, default=0)
    is_alive = Column(Boolean(), nullable=False, default=True)
    cooldawn_neck = Column(DateTime(), default=datetime.now)
    cooldawn_roulette = Column(DateTime(), default=datetime.now)


engine.connect()
base.metadata.create_all(engine)
