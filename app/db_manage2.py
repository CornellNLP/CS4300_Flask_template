from app import db
from app.irsystem.models import (
    Recipe, 
    Category, 
    RecipeCategorization
)
import json
from app.testdata import data
from sqlalchemy.exc import IntegrityError
from app.irsystem.controllers.search_controller import tokenize
import pandas as pd
import numpy as np
from sklearn import ensemble

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
Update recipes table to add recipe categories to recipes table and restore original capitalizations.
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


unique_categories = [] # unique categories of all recipe titles
title_words_set = [] # unique words in all recipe titles
title_to_index = {}
index_to_title = {}
recipe_titles = []
x_train = None # placeholder value
x_test = None # placeholder value
y_train = None # placeholder value
y_test = None # placeholder value
meal_dict = {"0" : "breakfast", "1": "lunch", "2": "dinner"}

"""
Update recipes table to include ML-determined meal type for each recipe, i.e.
"breakfast," "lunch," or "dinner."
"""
def add_categorizations():
  placeholder_exists = db.session.query(Category).filter_by(name="PLACEHOLDER XXX").first()
  if placeholder_exists is not None:
    return
  x_train, x_test, y_train, y_test = classify_recipes()
  c = Category(name="PLACEHOLDER XXX")
  db.session.add(c)
  db.session.flush()
  db.session.commit()
  i = 0
  for j in x_train.index:
    recipe = db.session.query(Recipe).filter_by(title=recipe_titles[j]).first()
    if recipe:
      recipe.meal_type = meal_dict[y_train[i]]
      db.session.flush()
      db.session.commit()
    i += 1
  i = 0
  for j in x_test.index:
    recipe = db.session.query(Recipe).filter_by(title=recipe_titles[j]).first()
    if recipe:
      recipe.meal_type = meal_dict[y_test[i]]
      db.session.flush()
      db.session.commit()
    i += 1


def classify_recipes():
  with open("app/full_format_recipes.json") as f:
    data = json.loads(f.readlines()[0])
    fill_data_structures(data)

    data_df1 = pd.DataFrame(columns = title_words_set, index = index_to_title.keys())
    data_df2 = pd.DataFrame(columns = unique_categories, index = index_to_title.keys())
    populate_matrices(data, data_df1, data_df2)

    breakfast_inds = np.where(data_df2["breakfast"] > 0)[0]
    lunch_inds = np.where(data_df2["lunch"] > 0)[0]
    dinner_inds = np.where(data_df2["dinner"] > 0)[0]
    breakfast_inds = [ind for ind in list(breakfast_inds) if ind not in lunch_inds and ind not in dinner_inds]
    lunch_inds = [ind for ind in list(lunch_inds) if ind not in breakfast_inds and ind not in dinner_inds]
    dinner_inds = [ind for ind in list(dinner_inds) if ind not in lunch_inds and ind not in breakfast_inds]

    del data_df2['breakfast']
    del data_df2['lunch']
    del data_df2['dinner']
    y_train = pd.DataFrame(columns = ["CLASS"], index = index_to_title.keys())
    y_train.loc[breakfast_inds,"CLASS"] = "0"
    y_train.loc[lunch_inds,"CLASS"] = "1"
    y_train.loc[dinner_inds,"CLASS"] = "2"
    y_train = y_train.dropna()

    data_df = pd.concat([data_df1, data_df2], axis=1)
    inds_train = breakfast_inds + lunch_inds + dinner_inds
    inds_train.sort()
    inds_train = data_df.index.isin(inds_train)
    x_train = data_df.iloc[inds_train,:]
    x_test = data_df.iloc[~inds_train,:]

    clf = ensemble.RandomForestClassifier(n_estimators = 100)
    clf.fit(x_train, y_train["CLASS"])
    y_train_pred = clf.predict(x_train)
    y_test_pred = clf.predict(x_test)
    return x_train, x_test, y_train_pred, y_test_pred


def fill_data_structures(data):
  j = 0
  for i in range(len(data)):
    if len(data[i]) == 11:
        title = data[i]['title']
        if title not in title_to_index:
            title_to_index[title] = []
            title_to_index[title].append(j)
        else:
            title_to_index[title].append(j)
        index_to_title[j] = title
        
        # add any new categories to set
        categs = data[i]['categories']
        for c in categs:
            c_l = c.lower()
            if c_l not in unique_categories:
                unique_categories.append(c_l)
                
        # add any new titles to set
        title_words = tokenize(title)
        for w in title_words:
            if w not in title_words_set:
                title_words_set.append(w)
        recipe_titles.append(title)
        j = j + 1


def populate_matrices(data, data_df1, data_df2):
  N = len(index_to_title) # number of total recipes
  for col in data_df1.columns:
      data_df1[col].values[:] = 0
  for col in data_df2.columns:
      data_df2[col].values[:] = 0

  # for each recipe
  i = 0
  for r in data:
      if len(r) == 11:
          title_words = tokenize(r['title'])
          category_words = r['categories']
          for word in title_words:
              data_df1[word][i] = data_df1[word][i] + 1
          for word in category_words:
              word = word.lower()
              data_df2[word][i] += 1
          if len(category_words) > 0:
              data_df2.iloc[i,:] = data_df2.iloc[i,:]/len(category_words)
          data_df1.iloc[i,:] = data_df1.iloc[i,:]/len(title_words)
          i += 1
          
  data_df1 = data_df1 * np.log(N / np.count_nonzero(data_df1, axis = 0) )
  data_df2 = data_df2 * np.log(N / np.count_nonzero(data_df2, axis = 0) )

