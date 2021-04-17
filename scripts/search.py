"""
Searches for recipes similar to movie and returns top ten. 
"""
import scripts.sim
import json
import pandas as pd

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


def mat_search(query, sim_mat, movie_to_index, recipe_list):

    if query not in movie_to_index:
        return "Sorry! Movie not found."
    query_index = movie_to_index[query]
    recipe_scores = sim_mat[query_index]
    recipe_tuples = []
    for i in range(len(recipe_list)):
        # print(recipe_list[i])
        recipe_tuples.append((i, recipe_scores[i]))
    results = sorted(recipe_tuples, key=(lambda x: x[1]), reverse=True)
    # results = [(r[1], r[0]) for r in sorted(recipe_tuples, reverse=True)]
    return results[:10]


def run_search(sim_mat, movie_list, query, recipes):
    # recipe_mat, vectorizer = sim.build_vectorizer(recipe_list)
    # movie_mat = sim.get_movie_tfidfs(movie_list, vectorizer)
    # sim_mat = sim.get_cos_sim(recipe_mat, movie_mat)

    movie_to_index = movie_to_index_maker(movie_list)

    res = mat_search(query, sim_mat, movie_to_index, recipes)

    return res


if __name__ == "__main__":
    # recipe_list = ["Double Cheeseburger", "Cheeseburger Sliders", "Pop-Tarts",
    #                "Blueberry Pancakes", "Shrimp and Catfish Gumbo", "Cajun Shrimp", "Shrimp Burgers"]
    # movie_list = {"Pulp Fiction": [
    #     "burger, cheeseburger"], "Forrest Gump": ["shrimp", "chocolates"]}
    query = "Forrest Gump"

    with open('./data/movie_food_words_from_wordnets.json') as f:
        movie_list = json.load(f)

    recipes = pd.read_csv('./data/recipe_data/clean_recipes.csv')
    movie_recipe_mat = pd.read_csv('./data/movie_recipe_mat.csv')

    run_search(movie_recipe_mat, movie_list, query, recipes)
