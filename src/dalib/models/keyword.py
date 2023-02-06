from sqlalchemy import Table, Column, Integer, String, DateTime, Float, MetaData, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Keyword(Base):
    __tablename__ = 'keyword'

    id = Column(Integer, primary_key=True)
    word = Column(String)    

    def __init__(self, word):
        self.word = word        