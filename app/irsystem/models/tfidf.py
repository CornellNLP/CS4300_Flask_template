from . import *

class TFIDF(Base):
  __tablename__ = 'tfidf'

  RowNo = db.Column(db.Integer, nullable=False)
  ColNo = db.Column(db.Integer, nullable=False)
  CellValue = db.Column(db.Float, nullable=False)

  def __repr__(self):
    return '<TFIDF Row is %r, Column is %r, Cell Value is %r>' % (self.RowNo, self.ColNo, self.CellValue)
    #print("Total score for %s is %s" % (name, score))


class TFIDFSchema(ModelSchema):
  class Meta:
    model = TFIDF



  