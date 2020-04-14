from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.jokes import *

project_name = "Haha Factory"
net_id = "Jason Jung: jj634, Suin Jung: sj575, Winice Hui: wh394, Cathy Xin: cyx5, Rachel Han: ryh25"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	min_score = request.args.get('score')

	if query == '' or query is None: 
		query = None 
	
	jokes = Joke.query.filter_by(score =  min_score).all()
    
	results = [
      {
        "text": joke.text,
        "categories": joke.categories,
        "score": str(joke.score),
        "maturity": joke.maturity,
      } for joke in jokes]
	

	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=results)



