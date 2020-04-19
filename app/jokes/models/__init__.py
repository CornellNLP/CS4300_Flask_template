from app import db # Grab the db from the top-level app
from marshmallow_sqlalchemy import ModelSchema # Needed for serialization in each model
import datetime # For handling dates 

class Base(db.Model):
  """Base PostgreSQL model: Base data model for all objects"""
  __abstract__ = True
  created_at = db.Column(db.DateTime, default    =db.func.current_timestamp())
  updated_at = db.Column(db.DateTime, default    =db.func.current_timestamp())
