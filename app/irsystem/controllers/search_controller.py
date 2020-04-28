from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import search_drinks
from app.irsystem.models.database import query_embeddings
import json

project_name = "Pick Your Poison"
net_id = """
Collin Montag (cm759),
Derek Cheng (dsc252),
DB Lee (dl654),
Dana Luong (dl697),
Ishneet Sachar (iks23)
"""

@irsystem.route('/descriptors', methods=['GET'])
def serve_desc():
	descriptors = sorted([e.word for e in query_embeddings()])
	descriptors = [d.replace('_', ' ') for d in descriptors]
	return render_template('desc_list.html', descriptors=descriptors)

@irsystem.route('/', methods=['GET'])
def search():

	page_number = request.args.get('page')
	drink_type = request.args.get('type')
	base = request.args.get('base')
	descriptors = request.args.get('descriptors')
	min_price = request.args.get('min-price')
	max_price = request.args.get('max-price')
	min_abv = request.args.get('min-abv')
	max_abv = request.args.get('max-abv')
	drink_name = request.args.get('drink') # for searching for similar drinks

	if drink_name:
		print("User searched for drinks similar to {}".format(drink_name))
		results = search_drinks(drink_name, k=10)

		if results is not None:
			return render_template('results.html', results=results, page_number=page_number, drink_name=drink_name)
	
	if drink_type and descriptors:
		desc_lst = [d.strip().lower().replace(' ', '_') for d in descriptors.split(',')]
		print("User searched for a {} with descriptors: {}".format(drink_type, descriptors))

		results = search_drinks(desc_lst, dtype=None if drink_type == 'anything' else drink_type, k=10)
		for i in range(len(results)):
			results[i][1] = json.loads(results[i][0].reviews) if results[i][0].reviews is not None else []

		if results is not None:
			return render_template('results.html', results=results, page_number=page_number, drink_type=drink_type, base=base, descriptors=descriptors, min_price=min_price, max_price=max_price)

	descriptors = [e.word.replace('_', ' ') for e in query_embeddings()]

	return render_template('search.html', descriptors=descriptors)
