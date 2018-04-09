from app import db # Grab the db from the top-level app
from marshmallow_sqlalchemy import ModelSchema # Needed for serialization in each model
from . import *

class Comment(Base):
  __tablename__ = 'comments'
  comment_id = db.Column(db.String, unique=True, nullable=False)
  author     = db.Column(db.String, nullable=False)
  subreddit  = db.Column(db.String, nullable=False)
  link_id    = db.Column(db.String, nullable=False)
  body       = db.Column(db.Text, nullable=False)
  score      = db.Column(db.Integer, nullable=False)
  gilded     = db.Column(db.Integer, nullable=False)
  upvotes    = db.Column(db.Integer, nullable=False)
  downvotes  = db.Column(db.Integer, nullable=False)

  def __init__(self, comment_id, author, subreddit, link_id, body, score, gilded, upvotes, downvotes):
    self.comment_id   = comment_id
    self.author       = author
    self.subreddit    = subreddit
    self.link_id      = link_id
    self.body         = body
    self.score        = score
    self.gilded       = gilded
    self.upvotes      = upvotes
    self.downvotes    = downvotes

  def __repr__(self):
    return str(self.__dict__)

class CommentSchema(ModelSchema):
  class Meta:
    model = Comment