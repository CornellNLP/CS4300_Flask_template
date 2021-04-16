from . import *

class Shoe(Base):
  __tablename__ = 'shoe'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable =False)
  price = db.Column(db.Float, nullable =False)
  rating = db.Column(db.Float, nullable=False)
  color = db.Column(db.String(128), nullable =False)
  description = db.Column(db.String(512), nullable =False, max_length=512)
  material = db.Column(db.String(128), nullable =False)
  fit = db.Column(db.String(128), nullable =False)
  brand = db.Column(db.String(128), nullable =False)
  img_url = db.Column(db.String(512), nullable=False, max_length=512)
  reviews = db.relationship('Review', backref='shoe', lazy=True)

  def __init__(self, **kwargs):
    self.name = kwargs.get('name', None)
    self.price = kwargs.get('price', None)
    self.rating = kwargs.get('rating', None)
    self.color = kwargs.get('color', None)
    self.description = kwargs.get('description', None)
    self.material = kwargs.get('material', None)
    self.fit = kwargs.get('fit', None)
    self.img_url = kwargs.get('img_url', None)
    self.brand = kwargs.get('brand', None)



  def __repr__(self):
    return str(self.__dict__)


class ShoeSchema(ModelSchema):
  class Meta:
    model = Shoe
