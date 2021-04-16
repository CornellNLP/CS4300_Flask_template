from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app import app as data_pool
import json

project_name = "Book Club"
net_id = "Caroline Lui: cel243, Elisabeth Finkel: esf76, Janie Walter: jjw249, Kurt Huebner: krh57, Taixiang(Max) Zeng: tz376"


### helpers ###
def _get_book_from_partial(works, book_str):
	"""Given a partial string `book_str`, returns a list of elements 
	("book_name by author", work_id, cover) where book_str is a substring
	of book_name. The HTML template can then use the strings, work_ids, 
	and cover image urls to display possible matches for the user to
	select between.
	"""
	relv_books = []
	book_str = book_str.lower()
	for work_id in works.keys():
		title = works[work_id]['title']
		if book_str in title.lower():
			authors = works[work_id].get("author_names", ["(unknown)"])
			authors = ", ".join(authors)
			string = f'"{title}" by {authors}'
			relv_books.append(
				{"string": string, "work_id": work_id, "image": works[work_id].get("image")}
			)
			# relv_books.append((title, works[work_id]['url']))
	return relv_books


def _get_reccs(works, selected_books):
	return ["harry potter is pretty good", "book2", "book3"]


### ajax endpoints ###

# GET request to search for matching book names
@irsystem.route('/booknames', methods=['GET'])
def get_book_from_partial():
	partial = request.args.get('partial')
	if not partial:
		return json.dumps([])
	return json.dumps(_get_book_from_partial(data_pool.works, partial))

# @irsystem.route('/booknames', methods=['GET'])
# def get_book_from_partial():
# 	partial = request.args.get('partial')
# 	if not partial:
# 		return json.dumps([])
# 	return json.dumps(["book title"])
	
	
### html endpoints ###

# Endpoint that receives preferences and displays result
@irsystem.route('/result', methods=['POST'])
def get_reccs():
	req = json.loads(request.data)
	liked_works = req.get('liked_works')

	results = _get_reccs(data_pool.works, liked_works)
	return "Result (template TBD): "+str(results)
	# return render_template('result.html', results=results), 200

# @irsystem.route('/result', methods=['POST'])
# def get_reccs():
# 	req = json.loads(request.data)
# 	liked_works = req.get('liked_works')

# 	results = ["abc", "def"]
# 	return "Result (template TBD): "+str(results)
# 	# return render_template('result.html', results=results)

# Route to select.html with num_users as parameter
@irsystem.route('/select', methods=['GET'])
def select():
	query = request.args.get('num_users')
	try:
		num_users = int(query)
		return render_template('select.html', users=num_users), 200 #, name=project_name, netid=net_id, output_message=output_message, data=data)
	except:
		return render_template('index.html'), 200

# Initial route to index.html
@irsystem.route('/', methods=['GET'])
def search():
	# query = request.args.get('search')
	# if not query:
	# 	data = []
	# 	output_message = ''
	# else:
	# 	output_message = "Your search: " + query
	# 	data = range(5)
	
	return render_template('index.html'), 200 #, name=project_name, netid=net_id, output_message=output_message, data=data)
