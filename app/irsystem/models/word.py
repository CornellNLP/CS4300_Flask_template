from . import *

class Word(Base):
  __tablename__ = 'word'
  index = db.Column(db.Integer, nullable=False)
  name = db.Column(db.String, nullable=False)
  #vectors = db.Column(db.Text, nullable=False)
  book_scores = db.Column(db.Text, nullable=False)
  word_scores = db.Column(db.Text, nullable=False)



  def __repr__(self):
    return '<Name: %r, Index: %r>' % (self.name, self.index)
    #print("Total score for %s is %s" % (name, score))


class Wordchema(ModelSchema):
  class Meta:
    model = Word



