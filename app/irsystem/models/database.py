import sys, os
sys.path.append(os.getcwd())
from app import db

class Drink(db.Model):
    __tablename__ = 'drink'
    name = db.Column(db.Text(), primary_key=True)
    description = db.Column(db.Text(), nullable=True)
    vbytes = db.Column(db.Text(), nullable=False)
    type = db.Column(db.Text(), nullable=False)
    price = db.Column(db.Float(), nullable=True)
    origin = db.Column(db.Text(), nullable=True)
    abv = db.Column(db.Float(), nullable=True)
    rating = db.Column(db.Text(), nullable=True)
    reviews = db.Column(db.Text(), nullable=True)
    url = db.Column(db.Text(), nullable=True)
    base = db.Column(db.Text(), nullable=True)

    def __repr__(self):
        return '<Drink {}>'.format(self.name)

class Embedding(db.Model):
    __tablename__ = 'embedding'
    word = db.Column(db.Text(), primary_key=True)
    vbytes = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return '<Embedding {}>'.format(self.word)

# Add a `Drink` object to database
def add_drink(drink):
    db.session.add(drink)
    db.session.commit()

# Add a list of `Drink` objects to database
def add_drink_batch(drinks):
    for d in drinks:
        if not contains_drink(d.name):
            db.session.add(d)
    db.session.commit()

# Add a list of `Embedding` objects to database
# Assumes unique set of words from 'embeddings/data/descriptor_mapping.csv'
def add_embedding_batch(embeddings):
    db.session.add_all(embeddings)
    db.session.commit()
    
def query_drink(dtype=None, pmin=None, pmax=None, amin=None, amax=None, base=None):
    q = db.session.query(Drink)
    if dtype is not None:
        q = q.filter(Drink.type == dtype)
    if pmin is not None:
        q = q.filter(Drink.price >= pmin)
    if pmax is not None:
        q = q.filter(Drink.price <= pmax)
    if amin is not None:
        q = q.filter(Drink.abv >= amin)
    if amax is not None:
        q = q.filter(Drink.abv <= amax)
    if base is not None:
        q = q.filter(Drink.base == base)
    return q.all()

def query_embeddings():
    return db.session.query(Embedding).all()

def contains_drink(name):
    q = db.session.query(Drink).filter(Drink.name == name)
    return db.session.query(q.exists()).scalar()

def query_drink_vbytes(name):
    d = db.session.query(Drink).get(name)
    return d.vbytes if d is not None else d
