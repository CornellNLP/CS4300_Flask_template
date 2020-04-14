from app import db

class Drink(db.Model):
    __tablename__ = 'test'
    name = db.Column(db.String(64), primary_key=True)
    description = db.Column(db.Text(), nullable=False)
    vector = db.Column(db.LargeBinary(), nullable=False)

    def __repr__(self):
        return '<Drink {}>'.format(self.name)

def add_drink(name, desc, v_bytes):
    d = Drink(name=name, description=desc, vector=v_bytes)
    db.session.add(d)
    db.session.commit()
    