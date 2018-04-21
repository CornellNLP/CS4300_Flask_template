from . import *

class Word(Base):
  __tablename__ = 'word'
  index = db.Column(db.Integer, nullable=False)
  name = db.Column(db.String, nullable=False)
  vector = db.Column(db.Text, nullable=False)



  def __repr__(self):
    return '<Name: %r, Index: %r>' % (self.name, self.index)
    #print("Total score for %s is %s" % (name, score))


class Wordchema(ModelSchema):
  class Meta:
    model = Word



  #we have ~250,000 books so if each row have 50 books we will be safely below 10,000 limit. 
  #start_index
  #names 
  #vector 