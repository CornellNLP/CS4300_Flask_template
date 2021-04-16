# from . import *
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import csv


app = Flask(__name__)
# app.config.from_object(os.environ["APP_SETTINGS"])
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wcagxrxkxecdnc:893178f88b43d944efb35e054a7f07281acb3edfc42a185aa4b53f1a447d83e0@ec2-18-206-20-102.compute-1.amazonaws.com:5432/d8kj6e91df3a2r'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Shoe(db.Model):
  __tablename__ = 'shoe'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable =False)
  price = db.Column(db.Float, nullable =False)
  rating = db.Column(db.Float, nullable=False)
  color = db.Column(db.String(128), nullable =False)
  description = db.Column(db.String(512), nullable =False, max_length=512)
  material = db.Column(db.String(128), nullable =False)
  fit = db.Column(db.String(128), nullable =False)
  brand = db.Column(db.String(128), nullable =False)
  img_url = db.Column(db.String(512), nullable=False, max_length=512)
  reviews = db.relationship('Review', backref='shoe', lazy=True)

  def __init__(self, **kwargs):
    self.name = kwargs.get('name', None)
    self.price = kwargs.get('price', None)
    self.rating = kwargs.get('rating', None)
    self.color = kwargs.get('color', None)
    self.description = kwargs.get('description', None)
    self.material = kwargs.get('material', None)
    self.fit = kwargs.get('fit', None)
    self.img_url = kwargs.get('img_url', None)
    self.brand = kwargs.get('brand', None)

class Review(db.Model):
  __tablename__ = 'review'
  id = db.Column(db.Integer, primary_key=True)
  shoe_id = db.Column(db.Integer, db.ForeignKey('shoe.id'), nullable=False)
  text = db.Column(db.String(512), nullable =False, max_length=512)

db.drop_all()
db.create_all()
with open('sneakers_page3.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            name = row['name']
            if name == 'N/A': continue
            # price = float(row['price'][1:]) if row['price'] != 'N/A' else 0
            rating = float(row['rating']) if row['rating'] != 'N/A' else 0.0
            color = row['color'] if row['color'] != 'N/A' else ""
            description = row['description'][:512] if row['description'] != 'N/A' else ""
            material = row['material'] if row['material'] != 'N/A' else ""
            fit = row['fit'] if row['fit'] != 'N/A' else ""
            brand = row['brand'] if row['brand'] != 'N/A' else ""
            img_url = row['image'] if row['image'] != 'N/A' else ""
            reviews = row['reviews'][:512] if row['reviews'] else ""

            if ' – ' in row['price']: #handle case '$120.00 – $130.00'
                  price = row['price'].split('.')[0][1:]
                  price = float(price)
            else:
                  price = float(row['price'][1:]) if row['price'] != 'N/A' else 0

            shoe = Shoe(name=name, 
                        price=price, 
                        rating=rating, 
                        color=color, 
                        description=description, 
                        material=material, 
                        fit=fit, 
                        brand=brand,
                        img_url=img_url)
            
            if reviews:
                  reviews = reviews.split(";")
                  for review_text in reviews:
                        review = Review(text=review_text)
                        shoe.reviews.append(review)
            
            db.session.add(shoe)
            db.session.commit()
            
        line_count += 1
    print(f'Processed {line_count} lines.')

#name	price	rating	num_reviews	color	description	material	fit	reviews	brand

# db.drop_all()
# db.create_all()
# shoe = Shoe(name='t', price=1, rating=2.3, color='color', description='des', material='mat', fit='fit', brand='brand')
# shoe.reviews.append(review)
# db.session.add(shoe)
# db.session.commit()
# review = Review(text='22')
# review = Review(text='300', shoe_id=1)
# shoe.reviews.append(review)
# db.session.add(shoe)
# db.session.commit()