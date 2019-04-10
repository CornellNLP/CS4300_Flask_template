from . import *

class User(Base):
  __tablename__ = 'users'

  email           = db.Column(db.String(128), nullable =False, unique =True)
  fname           = db.Column(db.String(128), nullable =False)
  lname           = db.Column(db.String(128), nullable =False)
  password_digest = db.Column(db.String(192), nullable =False)

  def __init__(self, **kwargs):
    self.email           = kwargs.get('email', None)
    self.fname           = kwargs.get('fname', None)
    self.lname           = kwargs.get('lname', None)
    self.password_digest = generate_password_hash(kwargs.get('password'), None)

  def __repr__(self):
    return str(self.__dict__)


class UserSchema(ModelSchema):
  class Meta:
    model = User
