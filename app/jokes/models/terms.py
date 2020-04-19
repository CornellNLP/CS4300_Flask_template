from . import *
# from sqlalchemy.orm import composite

# class tuple(object): 
#     def __init__(self, **kwargs):
#         self.id = kwargs.get('id')
#         self.tf = kwargs.get('tfidf')
      
class Terms(Base):
  """Model for the terms table"""
  __tablename__ = 'terms'

  term          = db.Column(db.Text, nullable =False, primary_key = True)
  joke_ids      = db.Column(db.ARRAY(db.Integer), nullable = False)
  tfs           = db.Column (db.ARRAY(db.Integer), nullable = False)
#   documents     = db.Column(
#                     CompositeArray(
#                         CompositeType(
#                             'id_tf',
#                             [
#                                 db.Column('id', db.Integer),
#                                 db.Column('tf', db.Integer)
#                             ]
#                         )
#                     )
#   , unique = True, nullable = False)

  def __init__(self, **kwargs):
    self.term        = kwargs.get('term')
    self.joke_ids    = kwargs.get('joke_ids')
    self.tfs         = kwargs.get('tfs')

  def __repr__(self):
    """Define a base way to print models"""
    return str(self.__dict__)


class TermsSchema(ModelSchema):
  class Meta:
    model = Terms

    