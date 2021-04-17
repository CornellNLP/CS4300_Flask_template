from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import scripts.sim 
from scripts.search import run_search
project_name = "Screen to Table"
net_id = "Olivia Zhu(oz28), Daniel Ye(dzy3), Shivank Nayak(sn532), Kassie Wang(klw242), Elizabeth Healy(eah255)"

#toy dataset
recipe_list = ["Double Cheeseburger", "Cheeseburger Sliders", "Pop-Tarts",
								"Blueberry Pancakes", "Shrimp and Catfish Gumbo", "Cajun Shrimp", "Shrimp Burgers"]
movie_list = {"Pulp Fiction": [
				"burger, cheeseburger"], "Forrest Gump": ["shrimp", "chocolates"]}

@irsystem.route('/')
def home():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
		return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
	else:
		output_message = "Your search: " + query
		data = run_search(recipe_list, movie_list, query)
		return redirect(url_for('irsystem.get_results', data=data))

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = run_search(recipe_list, movie_list, query)
		# data = mat_search(query, sim_mat, movie_to_index, recipe_list)
	# return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
	return redirect(url_for('irsystem.get_results', data=data))

@irsystem.route('/results/<data>')
def get_results(data):
	return render_template('results.html')

@irsystem.route('/recipe/<title>')
def get_recipe(title):
	title = title
	ingredients = ["apples", "oranges"]
	steps = ["cook", "clean"]
	return render_template('recipe.html', ingredients=ingredients, steps=steps)


