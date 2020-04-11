from . import *

class Joke(Base):
  __tablename__ = 'jokes'

  text           = db.Column(db.String(128), nullable =False, unique =True)
  categories           = db.Column(db.ARRAY(db.String(128)))
  score           = db.Column(db.Numeric(5), nullable =True)
  maturity = db.Column(db.Integer, nullable =True)

  def __init__(self, **kwargs):
    self.text           = kwargs.get('text', None)
    self.categories           = kwargs.get('categories', [])
    self.score           = kwargs.get('score', None)
    self.maturity = kwargs.get('maturity', None)

  def __repr__(self):
    return str(self.__dict__)


class JokeSchema(ModelSchema):
  class Meta:
    model = Joke