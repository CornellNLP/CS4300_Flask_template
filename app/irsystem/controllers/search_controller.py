from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import SearchEngine
from app.irsystem.models.shared_variables import create_dataset_or_structures
project_name = "Subreddit Recommender"
class_name = "CS 4300 Spring 2020"
search_engine = SearchEngine(create_dataset_or_structures)

@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    if not query:
        data = []
        output_message = ''
        response = ''
    else:
        data = search_engine.search(query)
        if not data:
            response = "response"
            output_message = "Sorry, we can't make a good suggestion with that post.  Try adding some more detail to your post!"
        else:
            response = ""
            output_message = "You might want to post in:"
    return render_template('search.html', name=project_name,
                           class_name=class_name, output_message=output_message,
                           data=data, query=query, response=response)
