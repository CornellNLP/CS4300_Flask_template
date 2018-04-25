from . import *

class Books(Base):
  __tablename__ = 'books'

  start_index = db.Column(db.Integer, nullable=False)
  names = db.Column(db.Text, nullable=False)
  vectors = db.Column(db.Text, nullable=False)




  def __repr__(self):
    return '<Name: %r, Index: %r>' % (self.name, self.start_index)
    #print("Total score for %s is %s" % (name, score))


class Bookschema(ModelSchema):
  class Meta:
    model = Books




  #we have ~250,000 books so if each row have 50 books we will be safely below 10,000 limit. 
  #start_index
  #names 
  #vector 