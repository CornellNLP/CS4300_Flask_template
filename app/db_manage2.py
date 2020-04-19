from app import db
from app.irsystem.models import (
    Recipe, 
    Category, 
    RecipeCategorization
)
import json
from app.testdata import data
from sqlalchemy.exc import IntegrityError

"""
Populate Postgres database with complete dataset, found in app/full_format_recipes.json.
"""
def populate_db():
  recipes_exist = db.session.query(Recipe).filter_by(id=1).first()
  if recipes_exist:
    return
  with open("app/full_format_recipes.json") as f:
    full_data = json.loads(f.readlines()[0])
    for d in full_data:
      if len(d) == 11:
        # add main recipe information
        directions = " ".join(d["directions"])
        ingredients = " ".join(d["ingredients"])
        recipe = Recipe(
            directions = directions,
            ingredients = ingredients,
            fat = d["fat"],
            date = d["date"],
            calories = d["calories"],
            description = d["desc"],
            protein = d["protein"],
            rating = d["rating"],
            title = d["title"],
            sodium = d["sodium"]
        )
        db.session.add(recipe)
        db.session.flush()
        db.session.commit()

        # add categories
        for category in d["categories"]:
          category_id = None
          try:
            c = Category(name=category)
            db.session.add(c)
            db.session.flush()
            db.session.commit()
            category_id = c.id
          except IntegrityError:
            db.session.rollback()
            existing_category = db.session.query(Category).filter_by(name=category).first()
            category_id = existing_category.id
          db.session.add(RecipeCategorization(
            recipe_id = recipe.id,
            category_id = category_id
          ))
          db.session.flush()
          db.session.commit()


"""
Update table to add recipe categories to recipes table and account for original 
capitalizations.
"""
def update_table():
  first_recipe = db.session.query(Recipe).filter_by(id=1).first()
  if first_recipe.categories is not None:
    return
  with open("app/full_format_recipes.json") as f:
    full_data = json.loads(f.readlines()[0])
    for i in range(3, len(full_data) + 1):
      d = full_data[i - 1]
      if len(d) == 11:
        directions = " ".join(d["directions"])
        ingredients = " ".join(d["ingredients"])
        categories = " ".join(d["categories"])
        recipe = db.session.query(Recipe).filter_by(id=i).first()

        # updating
        recipe.directions = directions
        recipe.ingredients = ingredients
        recipe.description = d["desc"]
        recipe.title = d["title"]
        recipe.categories = categories
        db.session.flush()
        db.session.commit()