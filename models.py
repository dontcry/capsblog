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
Blog 
'''
class Blog(db.Model):  
  __tablename__ = 'blog'

  id = Column(Integer, primary_key=True)
  title = Column(String) 

  def __init__(self, title): 
    self.title = title 

  def format(self):
    return {
      'id': self.id,
      'title': self.title }