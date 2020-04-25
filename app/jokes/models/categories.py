from . import *

class Categories(Base):
  """Model for the categories table"""
  __tablename__ = 'categories'

  category      = db.Column(db.Text, nullable = False, primary_key = True)
  joke_ids      = db.Column(db.ARRAY(db.Integer), nullable = False)

  def __init__(self, **kwargs):
    self.category      = kwargs.get('category')
    self.joke_ids      = kwargs.get('joke_ids')

  def __repr__(self):
    """Define a base way to print models"""
    return str(self.__dict__)


class CategoriesSchema(ModelSchema):
  class Meta:
    model = Categories