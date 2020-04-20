from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.jokes import *
import app.irsystem.controllers.cat_jaccard as sl
import app.irsystem.controllers.cos_sim as cos
import json

with open('./inv_idx_free.json') as f:
	inv_idx_free = json.load(f)

project_name = "Haha Factory"
net_id = "Jason Jung: jj634, Suin Jung: sj575, Winice Hui: wh394, Cathy Xin: cyx5, Rachel Han: ryh25"
search_params = {}

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	min_score = request.args.get('score')
	categories = request.args.get('category')

	search_params['min_score'] = min_score if min_score else ''
	search_params['categories'] = categories if categories else ''
	search_params['key_words'] = query if query else ''

	results = {}

	if categories:
		categories_list = [el.strip() for el in categories.split(",")]

		cat_jokes = {} #dictionary where key = category, value = array of doc_ids with that category
		for cat in categories_list: #for every category
			doc_lst = Categories.query.filter_by(category = cat).first() #get the record where category is equal to cat
			cat_jokes[cat] = doc_lst.joke_ids

		numer_dict = sl.get_rel_jokes(cat_jokes) #dictionary with key = joke_id and value = numerator

		rel_jokes = {} #dictionary where key = joke_id, value = joke
		for doc in numer_dict.keys():
			rel_jokes[doc] = Joke.query.filter_by(id = doc).first()

		results_cat = sl.jaccard_sim(categories_list, numer_dict, rel_jokes)

		for element in results_cat:
			doc_id = element[0]
			joke = rel_jokes[doc_id]
			sim_measure = (element[1])
			if doc_id not in results:
				results[doc_id] = ({"text": joke.text,"categories": joke.categories,"score": str(joke.score),"maturity": joke.maturity}, sim_measure)
	
	results_cos = {}

	if query:
		results_query = cos.fast_cossim(query, inv_idx_free)
		for element in results_query:
			doc_id = element[0]
			joke = Joke.query.filter_by(id = doc_id).first()
			sim_measure = element[1]
			results_cos[doc_id] = ({"text": joke.text, "categories": joke.categories,"score": str(joke.score),"maturity": joke.maturity}, sim_measure*0.5)

	results_final = {}
	for i in range(6408):
		if i in results and i in results_cos:
			results_final[i] = results[i][0], results[i][1]*0.5 + results_cos[i][1]*0.5
		elif i in results:
			results_final[i] = results[i][0], results[i][1] * 0.5
		elif i in results_cos:
			results_final[i] = results_cos[i][0], results_cos[i][1] * 0.5

	final = []
	if min_score:
		for joke in results_final:
			if results_final[joke][0]['score'] == 'None':
				final.append((results_final[joke][0], "Similarity: " + str(results_final[joke][1]*0.67)))
			else:
				if float(results_final[joke][0]['score']) >= float(min_score):
					final.append((results_final[joke][0], "Similarity: " + str(results_final[joke][1]*0.67 + (0.33/5*float(results_final[joke][0]['score'])))))
				else:
					final.append((results_final[joke][0], "Similarity: " + str(results_final[joke][1]*0.67 + (0.16/5*float(results_final[joke][0]['score'])))))
		jokes = Joke.query.filter(Joke.score >= min_score).all()
		blahblah = [
			({"text": joke.text, "categories": joke.categories,"score": str(joke.score),"maturity": joke.maturity}, "Similarity: " + str(0.16/5*float(joke.score))) for joke in jokes
		]
		final +=blahblah

	else:
		final = [(x[1][0], "Similarity: " + str(x[1][1])) for x in results_final.items()]

	final = sorted(final, key = lambda x : (x[1]), reverse = True)

	Joke.testFunct()

	return render_template('search.html', name=project_name, netid=net_id, output_message=search_params, data=final)

@irsystem.route('/react', methods=['GET'])
def sendhome():
	return render_template('index.html')
