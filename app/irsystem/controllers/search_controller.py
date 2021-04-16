from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import sim
project_name = "Screen to Table"
net_id = "Olivia Zhu(oz28), Daniel Ye(dzy3), Shivank Nayak(sn532), Kassie Wang(klw242), Elizabeth Healy(eah255)"

@irsystem.route('/', methods=['GET'])
def search():

	recipe_list = ["Double Cheeseburger", "Cheeseburger Sliders", "Pop-Tarts",
										"Blueberry Pancakes", "Shrimp and Catfish Gumbo", "Cajun Shrimp", "Shrimp Burgers"]
	movie_list = {"Pulp Fiction": [
					"burger, cheeseburger"], "Forrest Gump": ["shrimp", "chocolates"]}
	recipe_mat, vectorizer = sim.build_vectorizer(recipe_list)
	movie_mat = sim.get_movie_tfidfs(movie_list, vectorizer)
	sim_mat = sim.get_cos_sim(recipe_mat, movie_mat)

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

	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = mat_search(query, sim_mat, movie_to_index, recipe_list)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



