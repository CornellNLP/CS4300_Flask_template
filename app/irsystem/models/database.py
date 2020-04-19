import sys, os
sys.path.append(os.getcwd())
from app import db

class Drink(db.Model):
    __tablename__ = 'test'
    name = db.Column(db.String(64), primary_key=True)
    description = db.Column(db.Text(), nullable=False)
    price = db.Column(db.String(20), nullable=True)
    origin = db.Column(db.String(50), nullable=True)
    vbytes = db.Column(db.LargeBinary(), nullable=False)

    def __repr__(self):
        return "<Drink(name='%s', description='%s', price='%s', origin = '%s')>"\
            % (self.name, self.description, self.price, self.origin)


# Add a `Drink` object to database
def add_drink(drink):
    db.session.add(drink)
    db.session.commit()

# Add a list of `Drink` objects to database
def add_drink_batch(drinks):
    for d in drinks:
        db.session.add(d)
    db.session.commit()
    
def create_db():
    return db.session.query(Drink)