from . import *

class Authors(Base):
  __tablename__ = 'authors'

  start_index = db.Column(db.Integer, nullable=False)
  names = db.Column(db.Text, nullable=False)
  book_lists = db.Column(db.Text, nullable=False)




  def __repr__(self):
    return '<Name: %r, Index: %r>' % (self.names, self.start_index)
    #print("Total score for %s is %s" % (name, score))


class Authorschema(ModelSchema):
  class Meta:
    model = Authors
