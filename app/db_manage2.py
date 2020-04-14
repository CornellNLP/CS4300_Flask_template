from app import db
from app.irsystem.models import (
    Recipe, 
    Category, 
    Ingredient, 
    RecipeCategorization, 
    RecipeIngredient
)
import json
from app.testdata import data
from sqlalchemy.exc import IntegrityError

"""
with open("full_format_recipes.json") as f:
      data = json.loads(f.readlines()[0])
"""

def reset_db():
  db.drop_all()
  db.session.commit()

def populate_db():
  recipe_counter = 1
  category_counter = 1
  ingredient_counter = 1
  for d in data:
    if len(d) == 11:
      # add main recipe information
      directions = ""
      for step in d["directions"]:
        directions += step + " "
      db.session.add(Recipe(
          directions = directions,
          fat = d["fat"],
          date = d["date"],
          calories = d["calories"],
          description = d["desc"],
          protein = d["protein"],
          rating = d["rating"],
          title = d["title"],
          sodium = d["sodium"]
      ))
      db.session.commit()

      # add categories
      for c in d["categories"]:
        try:
          db.session.add(Category(
            name = c
          ))
          db.session.commit()
        except IntegrityError:
          db.session.rollback()
      
      # add ingredients
      for ingredient in d["ingredients"]:
        db.session.add(Ingredient(
          name = ingredient
        ))
        db.session.commit()
      
      # add recipe-category link
      db.session.add(RecipeCategorization(
        recipe_id = recipe_counter,
        category_id = category_counter
      ))
      db.session.commit()

      # add recipe-ingredient link
      db.session.add(RecipeIngredient(
        recipe_id = recipe_counter,
        ingredient_id = ingredient_counter
      ))
      db.session.commit()

      recipe_counter += 1
      category_counter += 1
      ingredient_counter += 1