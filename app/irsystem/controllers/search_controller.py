from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.jokes import *
import app.irsystem.controllers.output_res as ressy
import app.irsystem.controllers.cat_jaccard as jac
import app.irsystem.controllers.cos_sim as cos
import json

with open('./inv_idx_free.json') as f:
    inv_idx_free = json.load(f)

project_name = "Haha Factory"
net_id = "Jason Jung: jj634, Suin Jung: sj575, Winice Hui: wh394, Cathy Xin: cyx5, Rachel Han: ryh25"
search_params = {}


@irsystem.route('/', methods=['GET'])
def search():
	cat_options = [cat.category for cat in Categories.query.all()]

	query = request.args.get('search') #query = request.args.get('search', default= '')
	min_score = request.args.get('score')
	categories = request.args.getlist('category')
	
	search_params['min_score'] = min_score if min_score else ''
	search_params['categories'] = categories if categories else ''
	search_params['key_words'] = query if query else ''
	
	results_jac = {}  # dictionary key = joke_id, value = (joke_dict, jac_sim)
	
	if categories:
		categories_list = categories
		
		cat_jokes = {}  # dictionary where key = category, value = array of doc_ids with that category
		for cat in categories_list:  # for every category
			 # get the record where category is equal to cat
			doc_lst = Categories.query.filter_by(category=cat).first()
			cat_jokes[cat] = doc_lst.joke_ids

        # dictionary with key = joke_id and value = numerator
		numer_dict = jac.get_rel_jokes(cat_jokes)
		
		rel_jokes = {}  # dictionary where key = joke_id, value = joke
		for doc in numer_dict.keys():
			rel_jokes[doc] = Joke.query.filter_by(id=doc).first()
		
		results_cat = jac.jaccard_sim(categories_list, numer_dict, rel_jokes)
		
		
		for element in results_cat:
			doc_id = element[0]
			joke = rel_jokes[doc_id]
			sim_measure = (element[1])
			if doc_id not in results_jac:
				results_jac[doc_id] = ({"text": joke.text, "categories": joke.categories, "score": str(
					joke.score), "maturity": joke.maturity}, sim_measure)

    # dictionary where key= joke_id, value = (joke_dict, cos_sim)
	results_cos = {}
	
	if query:
        # a list of (joke_id, cos_sim)
		results_query = cos.fast_cossim(query, inv_idx_free)
		for element in results_query:
			doc_id = element[0]
			joke = Joke.query.filter_by(id=doc_id).first()
			sim_measure = element[1]
			results_cos[doc_id] = ({"text": joke.text, "categories": joke.categories, "score": str(
				joke.score), "maturity": joke.maturity}, sim_measure)
	
	results = ressy.weight(results_jac, results_cos)
	
	final = None
	if min_score:
		final = ressy.adj_minscore(float(min_score), results)
	else:
		# translate results into list without weighting for min_score
		final = [(x[1][0], "Similarity: " + str(x[1][1]))  for x in results.items()]

    # sort results by decreasing sim
	final = sorted(final, key=lambda x: (x[1]), reverse=True)
	cat_options = sorted(cat_options)

    # Joke.testFunct()
	return render_template('search.html', name=project_name, netid=net_id, output_message=search_params, data=final, cat_options = cat_options)


@irsystem.route('/react', methods=['GET'])
def sendhome():
    return render_template('index.html')
