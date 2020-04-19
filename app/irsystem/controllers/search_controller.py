from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.jokes import *
import app.irsystem.controllers.sim_lib as sl

project_name = "Haha Factory"
net_id = "Jason Jung: jj634, Suin Jung: sj575, Winice Hui: wh394, Cathy Xin: cyx5, Rachel Han: ryh25"
dictionary = {}

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	min_score = request.args.get('score')
    # categories = None # request.args.get('categories')

	if min_score is not None: 
		jokes = Joke.query.filter(Joke.score >=  min_score).all()
		results = [
			{
        "text": joke.text,
        "categories": joke.categories,
        "score": str(joke.score),
        "maturity": joke.maturity,
		} for joke in jokes]
	
        # # uncomment for jaccard sim on categories
        # """ 
        # results_cat = []
        # if categories is not None:
        #     cat_jokes = {} 
        #     for cat in categories:
        #         doc_lst = Joke.query.filter_by(category = cat).first()
        #         cat_jokes[cat] = doc_lst

        #     numer_dict = sl.get_rel_jokes(query, cat_jokes)
        #     rel_jokes = {}
        #     for doc in get_rel_jokes:
        #         rel_jokes[doc] = Joke.query.filter_by(id = doc).first()
        #     result_cat = jaccard_sim(numer_dict, rel_jokes)
        # """

	Joke.testFunct()

	if not query and not min_score:
		results = []
		output_message = ''
	else:
		output_message = "Your search: " + query
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=results)

@irsystem.route('/react', methods=['GET'])
def sendhome():
	return render_template('index.html')
