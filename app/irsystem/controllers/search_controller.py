from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import full_search

project_name = "Subreddit Recommender"
class_name = "CS 4300 Spring 2020"


@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    if not query:
        data = []
        output_message = ''
    else:
        # output_message = "Your search: " + query
        output_message = "You might want to post in:"
        data = full_search(query)
    return render_template('search.html', name=project_name, class_name=class_name, output_message=output_message, data=data)
