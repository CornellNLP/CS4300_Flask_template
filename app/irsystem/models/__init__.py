from app import db  # Grab the db from the top-level app
# Needed for serialization in each model
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import (
    Integer,
    String,
    Column,
    ForeignKey,
    DateTime,
    Float
)
from werkzeug import check_password_hash, generate_password_hash  # Hashing
import hashlib  # For session_token generation (session-based auth. flow)
import datetime  # For handling dates


class Base(db.Model):
    """Base PostgreSQL model"""
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class Recipe(Base):
    # recipes table
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    directions = Column(String(10000))
    fat = Column(Float)
    date = Column(DateTime)
    calories = Column(Float)
    description = Column(String())
    protein = Column(Float)
    rating = Column(Float)
    title = Column(String())
    sodium = Column(Float)


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True)


class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True)
    name = Column(String(800))


class RecipeCategorization(Base):
    __tablename__ = "recipe_categorizations"
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
