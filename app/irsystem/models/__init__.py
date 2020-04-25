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
from marshmallow import fields, Schema
from werkzeug import check_password_hash, generate_password_hash  # Hashing
import hashlib  # For session_token generation (session-based auth. flow)
import datetime  # For handling dates


class Base(db.Model):
    """Base PostgreSQL model"""
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class Recipe(Base):
    # recipes table
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    meal_type = Column(String())
    directions = Column(String())
    ingredients = Column(String())
    fat = Column(Float)
    date = Column(DateTime)
    calories = Column(Float)
    description = Column(String())
    protein = Column(Float)
    rating = Column(Float)
    title = Column(String())
    sodium = Column(Float)
    categories = Column(String())


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), unique=True)


class RecipeCategorization(Base):
    __tablename__ = "recipe_categorizations"
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))


class RecipeSchema(Schema):
    id = fields.Integer(dump_only=True)

    class Meta:
        ordered = False
        fields = (
            "id",
            "meal_type",
            "directions",
            "ingredients",
            "fat",
            "date",
            "calories",
            "description",
            "protein",
            "rating",
            "title",
            "sodium",
            "categories"
        )