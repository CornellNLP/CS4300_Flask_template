"""
Searches for recipes similar to movie and returns top ten. 
"""
import scripts.sim
import scripts.edit
import json
import pandas as pd
import csv

"""
Given a query (movie name), a dict of movies to food words, and a list of recipes
Step 1: generate or access similarity matrix
Step 2: use movie_name_to_index to retrieve row corresponding to query, or return error if movie not found
Step 3: use index_to_recipe to create list of tuples (similarity score, recipe), sort by similarity score,
return recipes in sorted order
"""

# load data
with open('./data/movie_food_words_from_wordnets_top2.json') as f:
    movie_list = json.load(f)
with open('./data/recipe_data/allergy_dict.json') as f:
    allergy_dict = json.load(f)
with open('./data/recipe_data/clean_recipes.csv') as f:
    csvreader = csv.DictReader(f, delimiter=';')
    recipes = []
    for row in csvreader:
        recipes.append(row)
with open('./data/movie_recipe_mat_top2.csv') as f:
    csvreader = csv.reader(f, delimiter=',')
    movie_recipe_mat = []
    for row in csvreader:
        movie_recipe_mat.append(row)
with open('./data/average_reviews.json') as f:
    reviews = json.load(f)
with open('./data/movie_script_list.txt') as f:
        titles = f.readlines()


def movie_to_index_maker(m_dict):
    m_to_i = {}
    m_list = [m for m in m_dict.keys()]
    for i in range(len(m_list)):
        m_to_i[m_list[i]] = i + 1
    return m_to_i


def get_rating(id, reviews):
    try:
        return reviews[str(float(id))]
    except:
        return 0


movie_to_index = movie_to_index_maker(movie_list)

def get_recipes_with_allergies(results, recipe_list,allergies, allergy_dict):
    allergy_list = [i.lower().strip() for i in allergies.split(',')]
    foods = set()
    for allergy in allergy_list:
        if allergy in allergy_dict:
            foods.update(allergy_dict[allergy])
        else:
            foods.add(allergy)
    foods = list(foods)
    top_10 = []
    for (idx, score, rating) in results:
        if len(top_10)==10:
            break
        ingredients = recipe_list[idx]["Ingredients"]
        allergy_ingredients = [item for item in foods if item in ingredients]
        if not allergy_ingredients:
            top_10.append((idx, score, rating))
    return top_10


def mat_search(query, sim_mat, movie_to_index, recipe_list, allergies, allergy_dict):

    if not validate_query(query):
        return None
    query_index = movie_to_index[query]
    recipe_scores = sim_mat[query_index]
    recipe_tuples = []
    for i in range(1, len(recipe_list)+1):
        recipe_tuples.append((i-1, recipe_scores[i],
            get_rating(recipe_list[i-1]["RecipeID"], reviews)))
    results = sorted(recipe_tuples, key=(lambda x: x[1]), reverse=True)
    
    if allergies:
        top = get_recipes_with_allergies(results, recipe_list,allergies, allergy_dict)
    else:
        top = results[:10]
        
    return sorted(top, key=(lambda x: x[2]), reverse=True)


def validate_query(query):
    return query in movie_to_index


def run_search(query, allergies):
    data = mat_search(query, movie_recipe_mat, movie_to_index, recipes,
     allergies, allergy_dict)

    if data == None:
        return data

    res = []
    for d in data:
        idx = int(d[0])
        rating = round(d[2],1) if d[2] else "n/a"
        r = recipes[idx]
        res.append((idx, r, rating))
    return res


def get_recipe(idx):
    return recipes[idx]

def get_closest(query):
    edits = scripts.edit.edit_distance_search(query, titles)
    topthree = edits[0][1] + "\n" + edits[1][1] + "\n" + edits[2][1]
    return edits[0][1]


if __name__ == "__main__":
    # recipe_list = ["Double Cheeseburger", "Cheeseburger Sliders", "Pop-Tarts",
    #                "Blueberry Pancakes", "Shrimp and Catfish Gumbo", "Cajun Shrimp", "Shrimp Burgers"]
    # movie_list = {"Pulp Fiction": [
    #     "burger, cheeseburger"], "Forrest Gump": ["shrimp", "chocolates"]}
    query = "Jacket"

    with open('./data/movie_food_words_from_wordnets_top2.json') as f:
        movie_list = json.load(f)

    #recipes = pd.read_csv('./data/recipe_data/clean_recipes.csv')
    with open('./data/recipe_data/clean_recipes.csv') as f:
        csvreader = csv.DictReader(f, delimiter=';')
        recipes = []
        for row in csvreader:
            recipes.append(row)
    with open('./data/average_reviews.json') as f:
        reviews = json.load(f)
    with open('./data/movie_script_list.txt') as f:
        titles = f.readlines()
    with open('./data/movie_recipe_mat_top2.csv') as f:
        csvreader = csv.reader(f, delimiter=',')
        movie_recipe_mat = []
        for row in csvreader:
            movie_recipe_mat.append(row)

    print(run_search(movie_recipe_mat, movie_list, query, recipes, reviews))
