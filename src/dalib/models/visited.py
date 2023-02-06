from sqlalchemy import Table, Column, Integer, String, DateTime, Float, MetaData, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Visited(Base):
    __tablename__ = 'visited'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    date_visit = Column(DateTime)

    def __str__(self):
        res = f"{self.url}-{self.date_visit}"
        return res

    def __init__(self, url="", date_visit=0):
        self.url = url
        self.date_visit = date_visit