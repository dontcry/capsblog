import os
import json
from sqlalchemy import Column, String, create_engine, Integer
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
''' 
def setup_db(app):
    app.config.from_object('config') 
    if "DATABASE_URL" in os.environ: 
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URL']
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Actor 
'''
class Actor(db.Model):  
  __tablename__ = 'actor'

  id = Column(Integer, primary_key=True)
  name = Column(String) 
  age = Column(String) 
  gender = Column(String) 
  photo = Column(String)  

  def __init__(self, name): 
    self.name = name 

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'gender': self.gender,
      'age': self.age,
      'photo': self.photo}
   
  def insert(self):
      db.session.add(self)
      db.session.commit()

  def update(self):
      db.session.commit()


  def delete(self):
      db.session.delete(self)
      db.session.commit()
'''
Movie 
'''
class Movie(db.Model):  
  __tablename__ = 'movie'

  id = Column(Integer, primary_key=True)
  title = Column(String) 
  release_date = Column(String) 
  poster = Column(String)  

  def __init__(self, title): 
    self.title = title 

  def format(self):
        return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date,
      'poster': self.poster}
   
  def insert(self):
      db.session.add(self)
      db.session.commit()

  def update(self):
      db.session.commit()


  def delete(self):
      db.session.delete(self)
      db.session.commit()

'''
Cast 
'''
class Cast(db.Model):  
  __tablename__ = 'cast'

  id = Column(Integer, primary_key=True)
  actor_id = Column(String) 
  movie_id = Column(String)  
 
 
 