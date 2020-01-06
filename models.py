import os
from sqla_wrapper import SQLAlchemy

db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite"))

class User(db.Model):
  # Login infoirmation
  email = db.Column(db.String, unique=True)
  password = db.Column(db.String)
  token = db.Column(db.String)
  uid = db.Column(db.Integer, primary_key=True)
  
  #additional user data
  name = db.Column(db.String)
  
  #For game playing
  secret_number = db.Column(db.Integer)