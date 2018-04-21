from . import *

class Book(Base):
  __tablename__ = 'book'

  index = db.Column(db.Integer, nullable=False)
  name = db.Column(db.String, nullable=False)
  vector = db.Column(db.Text, nullable=False)




  def __repr__(self):
    return '<Name: %r, Index: %r>' % (self.name, self.index)
    #print("Total score for %s is %s" % (name, score))


class Bookchema(ModelSchema):
  class Meta:
    model = Book



  