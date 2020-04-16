from app import db

class Drink(db.Model):
    __tablename__ = 'test'
    name = db.Column(db.String(64), primary_key=True)
    description = db.Column(db.Text(), nullable=False)
    vbytes = db.Column(db.LargeBinary(), nullable=False)

    def __repr__(self):
        return '<Drink {}>'.format(self.name)

# Add a `Drink` object to database
def add_drink(drink):
    db.session.add(drink)
    db.session.commit()

# Add a list of `Drink` objects to database
def add_drink_batch(drinks):
    for d in drinks:
        db.session.add(d)
    db.session.commit()
    