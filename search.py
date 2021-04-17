"""
Searches for recipes similar to movie and returns top ten. 
"""
import sim

"""
Given a query (movie name), a dict of movies to food words, and a list of recipes
Step 1: generate or access similarity matrix
Step 2: use movie_name_to_index to retrieve row corresponding to query, or return error if movie not found
Step 3: use index_to_recipe to create list of tuples (similarity score, recipe), sort by similarity score,
return recipes in sorted order
"""
##test case
recipe_list = ["Double Cheeseburger", "Cheeseburger Sliders", "Pop-Tarts",
                   "Blueberry Pancakes", "Shrimp and Catfish Gumbo", "Cajun Shrimp", "Shrimp Burgers"]
movie_list = {"Pulp Fiction": [
        "burger, cheeseburger"], "Forrest Gump": ["shrimp", "chocolates"]}
recipe_mat, vectorizer = sim.build_vectorizer(recipe_list)
movie_mat = sim.get_movie_tfidfs(movie_list, vectorizer)
sim_mat = sim.get_cos_sim(recipe_mat, movie_mat)

query = "Forrest Gump"

def movie_to_index_maker(m_dict):
    m_to_i = {}
    m_list = [m for m in m_dict.keys()]
    for i in range(len(m_list)):
        m_to_i[m_list[i]] = i
    return m_to_i

movie_to_index = movie_to_index_maker(movie_list)


def mat_search(query, sim_mat, movie_to_index, recipe_list):
    if query not in movie_to_index:
        return "Sorry! Movie not found."
    query_index = movie_to_index[query]
    recipe_scores = sim_mat[query_index]
    recipe_tuples = []
    for i in range(len(recipe_list)):
        recipe_tuples.append((recipe_scores[i], recipe_list[i]))
    results = [(r[1], r[0]) for r in sorted(recipe_tuples, reverse=True)]
    return results[:10]

print(mat_search(query, sim_mat, movie_to_index, recipe_list))


