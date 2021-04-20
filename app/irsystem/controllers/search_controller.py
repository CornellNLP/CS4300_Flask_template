from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import json
import pandas as pd
import csv
import scripts.sim as sim
from scripts.search import run_search
project_name = "Screen to Table"
net_id = "Olivia Zhu(oz28), Daniel Ye(dzy3), Shivank Nayak(sn532), Kassie Wang(klw242), Elizabeth Healy(eah255)"

# toy dataset
# recipe_list = ["Double Cheeseburger", "Cheeseburger Sliders", "Pop-Tarts",
# 								"Blueberry Pancakes", "Shrimp and Catfish Gumbo", "Cajun Shrimp", "Shrimp Burgers"]
# movie_list = {"Pulp Fiction": [
# 				"burger, cheeseburger"], "Forrest Gump": ["shrimp", "chocolates"]}

with open('./data/movie_food_words_from_wordnets.json') as f:
    movie_list = json.load(f)
with open('./data/recipe_data/clean_recipes.csv') as f:
    csvreader = csv.DictReader(f, delimiter=';')
    recipes = []
    for row in csvreader:
        recipes.append(row)
with open('./data/movie_recipe_mat.csv') as f:
    csvreader = csv.reader(f, delimiter=',')
    movie_recipe_mat = []
    for row in csvreader:
        movie_recipe_mat.append(row)
# recipes = pd.read_csv('./data/recipe_data/clean_recipes.csv', sep=';')
# movie_recipe_mat = pd.read_csv('./data/movie_recipe_mat.csv')
# print(recipes)
# print(movie_recipe_mat)


@irsystem.route('/', methods=['GET'])
def home():
    query = request.args.get('search')
    if not query:
        data = []
        output_message = ''
        return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
    else:
        output_message = "Your search: " + query
        res = run_search(movie_recipe_mat, movie_list, query, recipes)
        if res == None:
            output_message = res
            return render_template('search.html', name=project_name, netid=net_id, output_message=output_message)
        else:
            data = json.dumps(res)
            return redirect(url_for('irsystem.get_results', data=data))


# @irsystem.route('/', methods=['GET'])
# def search():
#     query = request.args.get('search')
#     if not query:
#         data = []
#         output_message = ''
#     else:
#         output_message = "Your search: " + query
#         data = run_search(sim_mat, movie_list, query)
#         # data = mat_search(query, sim_mat, movie_to_index, recipe_list)
#     # return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
#     return redirect(url_for('irsystem.get_results', data=data))


@irsystem.route('/results/<data>')
def get_results(data):
    res = []
    print(data)
    data = json.loads(data)
    for d in data:
        idx = int(d[0])
        r = recipes[idx]
        res.append((idx, r))
    return render_template('results.html', res=res)


@irsystem.route('/recipe/<idx>')
def get_recipe(idx):
    idx = int(idx)
    recipe = recipes[idx]
    title = recipe['Recipe Name']
    ingredients = recipe['Ingredients']
    steps = recipe['Directions']
    # title = 'Recipe Name'
    # ingredients = 'Ingredients'
    # steps = 'Directions'
    return render_template('recipe.html', title=title, ingredients=ingredients, steps=steps)
