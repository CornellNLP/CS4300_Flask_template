from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app import app as data_pool

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
			relv_books.append((string, work_id, works[work_id].get("image")))
			# relv_books.append((title, works[work_id]['url']))
	return relv_books


def _get_reccs(works, selected_books):
	return []


### ajax endpoints ###

@irsystem.route('/booknames', methods=['GET'])
def get_book_from_partial():
	partial = request.args.get('partial')
	if not partial:
		return json.dumps([])
	return json.dumps(_get_book_from_partial(data_pool.works, partial))
	
	
### html endpoints ###

@irsystem.route('/recommendations', methods=['POST'])
def get_reccs():
	req = json.loads(request.data)
	liked_works = req.get('liked_works')

	results = _get_reccs(data_pool.works, liked_works)
	# return render_template('result.html', results=results)


@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = range(5)
	
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
