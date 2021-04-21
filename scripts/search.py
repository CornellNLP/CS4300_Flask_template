"""
Searches for recipes similar to movie and returns top ten. 
"""
import scripts.sim
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
    

def mat_search(query, sim_mat, movie_to_index, recipe_list, reviews):

    if query not in movie_to_index:
        return None
    query_index = movie_to_index[query]
    # print(query_index)
    recipe_scores = sim_mat[query_index]
    recipe_tuples = []
    for i in range(1, len(recipe_list)+1):
        recipe_tuples.append((i-1, recipe_scores[i]))
    results = sorted(recipe_tuples, key=(lambda x: x[1]), reverse=True)
    top = results[:10]
    return sorted(top, key=(lambda x: get_rating(recipe_list[x[0]]["RecipeID"], reviews)), reverse = True)


def run_search(sim_mat, movie_list, query, recipes, reviews):
    movie_to_index = movie_to_index_maker(movie_list)
    res = mat_search(query, sim_mat, movie_to_index, recipes, reviews)

    return res


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
    with open('./data/movie_recipe_mat_top2.csv') as f:
        csvreader = csv.reader(f, delimiter=',')
        movie_recipe_mat = []
        for row in csvreader:
            movie_recipe_mat.append(row)

    print(run_search(movie_recipe_mat, movie_list, query, recipes, reviews))
