from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import SearchEngine

project_name = "Subreddit Recommender"
class_name = "CS 4300 Spring 2020"
search_engine = SearchEngine(False)


@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    if not query:
        data = []
        result_header_message = ''
        error_message = ''
        response = ''
    else:
        data = search_engine.search(query)
        if not data:
            response = "response"
            result_header_message = ""
            error_message = "Sorry, we can't make a good suggestion with that post.  Try adding some more detail to your post!"
        else:
            response = ""
            result_header_message = "Post in:"
            error_message = ""
    return render_template('search.html', name=project_name,
                           class_name=class_name, result_header_message=result_header_message,
                           error_message=error_message,
                           data=data, query=query, response=response)
