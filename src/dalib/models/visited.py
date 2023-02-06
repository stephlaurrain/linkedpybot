from sqlalchemy import Table, Column, Integer, String, DateTime, Float, MetaData, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Visited(Base):
    __tablename__ = 'visited'

    id = Column(Integer, primary_key=True)
    linkedin_id = Column(String)
    date_visit = Column(DateTime)

    def __str__(self):
        res = f"{self.linkedin_id}-{self.date_visit}"
        return res

    def __init__(self, linkedin_id="", date_visit=0):
        self.linkedin_id = linkedin_id
        self.date_visit = date_visit