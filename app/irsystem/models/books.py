from . import *

class Books(Base):
  __tablename__ = 'books'

  index = db.Column(db.Integer, nullable=False)
  name = db.Column(db.Text, nullable=False)
  word_cloud = db.Column(db.Text, nullable=False)
  vector = db.Column(db.Text, nullable = False)
  avg_rating = db.Column(db.Float, nullable=True)
  description = db.Column(db.Text, nullable=True)
  author = db.Column(db.Text, nullable=True)
  isbn10   = db.Column(db.String(30), nullable=True)
  isbn13 = db.Column(db.String(30), nullable=True)
  link = db.Column(db.Text, nullable=True)




  def __repr__(self):
    return '<Name: %r, Index: %r>' % (self.names, self.index)
    #print("Total score for %s is %s" % (name, score))


class Bookschema(ModelSchema):
  class Meta:
    model = Books




  #we have ~250,000 books so if each row have 50 books we will be safely below 10,000 limit. 
  #start_index
  #names 
  #vector 