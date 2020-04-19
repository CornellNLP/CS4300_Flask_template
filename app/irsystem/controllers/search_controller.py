from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.jokes import *
import app.irsystem.controllers.sim_lib as sl

project_name = "Haha Factory"
net_id = "Jason Jung: jj634, Suin Jung: sj575, Winice Hui: wh394, Cathy Xin: cyx5, Rachel Han: ryh25"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	min_score = request.args.get('score')
	categories = request.args.get('category')

	results = []

	if min_score is not None:
		jokes = Joke.query.filter(Joke.score >= min_score).all()
		results += [
			{
        "text": joke.text,
        "categories": joke.categories,
        "score": str(joke.score),
        "maturity": joke.maturity,
		} for joke in jokes]

    # uncomment for jaccard sim on categories
	if categories is not None:
		categories = [el.strip() for el in categories.split(",")]
		       
		cat_jokes = {} #dictionary where key = category, value = array of doc_ids with that category
		for cat in categories: #for every category
			doc_lst = Categories.query.filter_by(category = cat).first() #get the record where category is equal to cat
			cat_jokes[cat] = doc_lst.joke_ids
		
		numer_dict = sl.get_rel_jokes(cat_jokes) #dictionary with key = joke_id and value = numerator
		
		rel_jokes = {} #dictionary where key = joke_id, value = joke
		for doc in numer_dict.keys():
			rel_jokes[doc] = Joke.query.filter_by(id = doc).first()
		
		results_cat = sl.jaccard_sim(categories, numer_dict, rel_jokes)

		for element in results_cat: 
			doc_id = element[0]
			joke = rel_jokes[doc_id]
			sim_measure = "JACCARD SIM: %s" % (element[1])

			results.append((
			{
				"text": joke.text,
        		"categories": joke.categories,
       			 "score": str(joke.score),
        		"maturity": joke.maturity,
			}, sim_measure))

	Joke.testFunct()

	if not query and not min_score and not categories:
		results = []
		output_message = ''
	else:
		output_message = "Your search: " + query
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=results)

@irsystem.route('/react', methods=['GET'])
def sendhome():
	return render_template('index.html')