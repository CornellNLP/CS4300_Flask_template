from . import *

class Words(Base):
  __tablename__ = 'words'
  index       = db.Column(db.Integer, nullable=False)
  name        = db.Column(db.String,  nullable=False)
  book_scores = db.Column(db.Text,    nullable=False)



  def __repr__(self):
    return '<Name: %r, Index: %r>' % (self.name, self.index)
    #print("Total score for %s is %s" % (name, score))


class Wordschema(ModelSchema):
  class Meta:
    model = Words



