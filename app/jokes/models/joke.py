from . import *

class Joke(Base):
  """Model for the jokes table"""
  __tablename__ = 'jokes'

  text          = db.Column(db.Text, nullable =False)
  categories    = db.Column(db.ARRAY(db.Text))
  score         = db.Column(db.Numeric(5,4), nullable =True)
  maturity      = db.Column(db.Integer, nullable =True)

  def __init__(self, **kwargs):
    self.text           = kwargs.get('text')
    self.categories     = kwargs.get('categories', [])
    self.score          = kwargs.get('score', None)
    self.maturity = kwargs.get('maturity', None)

  def __repr__(self):
    """Define a base way to print models"""
    return str(self.__dict__)

  @classmethod
  def testFunct(cls):
    print('test')

  


class JokeSchema(ModelSchema):
  class Meta:
    model = Joke
    fields = ('text', 'categories', 'score', 'maturity')  # Serialize these fields

    