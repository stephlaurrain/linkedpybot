import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine, func,case
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from dalib.models.keyword import Keyword
from dalib.models.visited import Visited
import utils.date_utils as date_utils

class Dbcontext:
    
    def __init__(self, log):
        self.log = log            

    def set_dbpath(self, dbpath):
        self.engine = create_engine(f"sqlite:///{dbpath}")

    def connect(self):
        self.connection = self.engine.connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()     

    def get_visited_obj(self):
        return Visited()
    # get all
    def get_visited_list(self):
        return self.session.query(Visited).order_by(Visited.score).all()

    #EXEMPLE DE CASE, de STRFTOME et de count sur SQLALCHEMY
    # desc : order_by( Visited.date_first_visit.desc()).all()
    def get_visited_stats(self):
        my_case_stmt = case(
        [
            (func.strftime("%w",Visited.date_first_visit)=="0", "Dimanche"),              
            (func.strftime("%w",Visited.date_first_visit)=="1", "Lundi"),
            (func.strftime("%w",Visited.date_first_visit)=="2", "Mardi"),
            (func.strftime("%w",Visited.date_first_visit)=="3", "Mercredi"),
            (func.strftime("%w",Visited.date_first_visit)=="4", "Jeudi"),
            (func.strftime("%w",Visited.date_first_visit)=="5", "Vendredi"),
            (func.strftime("%w",Visited.date_first_visit)=="6", "Samedi")
        ]
        )
        return self.session.query(my_case_stmt,func.strftime("%d-%m-%Y",Visited.date_first_visit),func.count(1)).\
            group_by(func.strftime("%d-%m-%Y", Visited.date_first_visit)).order_by( Visited.date_first_visit).all()
    
    def get_keyword_list(self):
        return self.session.query(Keyword).order_by(Keyword.word).all()
    
    
    #count
    def visited_count(self):                
        return self.session.query(Visited).count()
    
    # is in
    def is_in_visited(self, linkedin_id):
        return bool(self.session.query(Visited).filter_by(linkedin_id=linkedin_id).first())
    
    def is_in_visited_recently(self, linkedin_id, days):
        datemax = date_utils.get_now_minus_days_at_mn(days=days)
        return bool(self.session.query(Visited).filter(and_(Visited.linkedin_id==linkedin_id, Visited.date_visit>datemax)).first())
     
    def add_to_keyword(self, word):
        keyword = Keyword(word=word)        
        self.session.add(keyword)  
        self.session.commit()

    def is_in_keyword(self, word):
        return bool(self.session.query(Keyword).filter_by(word=word).first())
        
    def get_visited_line(self, linkedin_id):     
        res = self.session.query(Visited).filter(Visited.linkedin_id==linkedin_id).first()
        return res

    # clean
    def clean_visited(self):        
        self.session.query(Visited).delete()
        self.session.commit()
        
    def clean_favorite(self):        
        self.session.query(Favorite).delete()
        self.session.commit()

    def add_to_visited(self, visited):                
        self.session.add(visited)  
        self.session.commit() 

    def vacuum(self):
        self.connection.execute("VACUUM")

    def rollback(self):
        self.session.rollback()

    # disconnection        
    def disconnect(self):
        #self.session.rollback()
        self.session.close()
        self.session.bind.dispose()
        self.connection.close()
        
        self.engine.dispose()

        
                

