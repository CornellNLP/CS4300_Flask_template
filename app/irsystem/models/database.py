import sys, os
sys.path.append(os.getcwd())
from app import db

class Drink(db.Model):
    __tablename__ = 'drink'
    name = db.Column(db.Text(), primary_key=True)
    description = db.Column(db.Text(), nullable=True)
    vbytes = db.Column(db.LargeBinary(), nullable=False)
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
    vbytes = db.Column(db.LargeBinary(), nullable=False)

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
    
def query_drink(dtype=None):
    if dtype is None:
        return db.session.query(Drink)
    return db.session.query(Drink).filter(Drink.type == dtype)

def query_embeddings():
    return db.session.query(Embedding)

def contains_drink(name):
    q = db.session.query(Drink).filter(Drink.name == name)
    return db.session.query(q.exists()).scalar()
