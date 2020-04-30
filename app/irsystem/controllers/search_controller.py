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

def arg_exists(arg):
	return arg is not None and arg != ''

@irsystem.route('/descriptors', methods=['GET'])
def serve_desc():
	descriptors = sorted([e.word for e in query_embeddings()])
	descriptors = [d.replace('_', ' ') for d in descriptors]
	return render_template('desc_list.html', descriptors=descriptors)

@irsystem.route('/search', methods=['GET'])
def search():
	page_number = request.args.get('page')
	page_number = int(page_number) if arg_exists(page_number) else 1
	drink_type = request.args.get('type')
	base = request.args.get('base')
	base = base if arg_exists(base) else None
	descriptors = request.args.get('descriptors')
	min_price = request.args.get('minprice')
	min_price = float(min_price) if arg_exists(min_price) else None
	max_price = request.args.get('maxprice')
	max_price = float(max_price) if arg_exists(max_price) else None
	min_abv = request.args.get('minabv')
	min_abv = float(min_abv) if arg_exists(min_abv) else None
	max_abv = request.args.get('maxabv')
	max_abv = float(max_abv) if arg_exists(max_abv) else None
	drink_name = request.args.get('drink') # for searching for similar drinks

	if drink_name:
		print("User searched for drinks similar to {}".format(drink_name))
		results, count = search_drinks(
			data=drink_name,
			k=10,
			page=page_number,
			pmin=min_price,
			pmax=max_price,
			amin=min_abv,
			amax=max_abv,
			base=base
		)
		
		if results is None:
			results = []
		return render_template('results.html', results=results, count=count, page_number=page_number, drink_name=drink_name)
	
	if type(descriptors) == list:
		desc_lst = [d.strip().lower().replace(' ', '_') for d in descriptors.split(',')]
		print("User searched for a {} with descriptors: {}".format(drink_type, descriptors))

		results, count = search_drinks(
			data=desc_lst,
			dtype=None if drink_type == 'anything' else drink_type,
			k=10,
			page=page_number,
			pmin=min_price,
			pmax=max_price,
			amin=min_abv,
			amax=max_abv,
			base=base
		)

		if results is None:
			results = []
		return render_template('results.html', results=results, count=count, page_number=page_number, drink_type=drink_type, base=base, descriptors=descriptors, min_price=min_price, max_price=max_price)

	results, count = search_drinks(
		data=None,
		dtype=None if drink_type == 'anything' else drink_type,
		k=10,
		page=page_number,
		pmin=min_price,
		pmax=max_price,
		amin=min_abv,
		amax=max_abv,
		base=base
	)

	if results is None:
		results = []
	return render_template('results.html', results=results, count=count, page_number=page_number, drink_type=drink_type, base=base, descriptors=descriptors, min_price=min_price, max_price=max_price)

@irsystem.route('/', methods=['GET'])
def home():
	descriptors = [e.word.replace('_', ' ') for e in query_embeddings()]
	return render_template('search.html', descriptors=descriptors)
