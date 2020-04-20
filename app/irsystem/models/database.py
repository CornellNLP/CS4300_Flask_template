import sys, os
sys.path.append(os.getcwd())
from app import db

class Drink(db.Model):
    __tablename__ = 'drink'
    name = db.Column(db.Text(), primary_key=True)
    description = db.Column(db.Text(), nullable=False)
    vbytes = db.Column(db.LargeBinary(), nullable=False)
    type = db.Column(db.Text(), nullable=False)
    price = db.Column(db.Integer(), nullable=True)
    origin = db.Column(db.Text(), nullable=True)

    def __repr__(self):
        return '<Drink {}>'.format(self.name)

# Add a `Drink` object to database
def add_drink(drink):
    db.session.add(drink)
    db.session.commit()

# Add a list of `Drink` objects to database
def add_drink_batch(drinks):
    for d in drinks:
        if not contains(d.name):
            db.session.add(d)
    db.session.commit()
    
def query_drink(dtype=None):
    if dtype is None:
        return db.session.query(Drink)
    return db.session.query(Drink).filter(Drink.type == dtype)

def contains(name):
    q = db.session.query(Drink).filter(Drink.name == name)
    return db.session.query(q.exists()).scalar()
