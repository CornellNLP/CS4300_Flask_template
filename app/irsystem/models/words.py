from . import *

class Words(Base):
  __tablename__ = 'words'
  start_index = db.Column(db.Integer, nullable=False)
  names = db.Column(db.Text, nullable=False)
  vectors = db.Column(db.Text, nullable=False)



  def __repr__(self):
    return '<Name: %r, Index: %r>' % (self.name, self.start_index)
    #print("Total score for %s is %s" % (name, score))


class Wordschema(ModelSchema):
  class Meta:
    model = Words



