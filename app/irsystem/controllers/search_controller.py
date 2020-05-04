from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import search_drinks, Args
from app.irsystem.models.database import query_embeddings, query_drink, Drink
from flask import jsonify
from uuid import uuid4
import json

PAGE_K = 10 # Number of results displayed per page
CACHE_SIZE = 100 # Number of results held in cache

def get_sid():
	if session.get('sid', None) is None:
		session['sid'] = uuid4()
	return session['sid']

def conv_arg(arg, conv):
	return conv(arg) if arg is not None and arg != '' else None

def make_args(args):
	dname = conv_arg(args.get('drink'), str)
	descriptors = conv_arg(args.get('descriptors'), str)
	desc_lst = [d.strip().lower().replace(' ', '_') for d in descriptors.split(',')] if descriptors is not None else None
	dtype = conv_arg(args.get('type'), str)
	return Args(
		data=dname if dname is not None else desc_lst,
		dtype=dtype if dtype != 'anything' else None,
		pmin=conv_arg(args.get('minprice'), float),
		pmax=conv_arg(args.get('maxprice'), float),
		amin=conv_arg(args.get('minabv'), float),
		amax=conv_arg(args.get('maxabv'), float),
		base=conv_arg(args.get('base'), str)
	)

@irsystem.route('/descriptors', methods=['GET'])
def serve_desc():
	descriptors = sorted([e.word for e in query_embeddings()])
	descriptors = [d.replace('_', ' ') for d in descriptors]
	return render_template('desc_list.html', descriptors=descriptors)

@irsystem.route('/search', methods=['GET'])
def search():
	more = conv_arg(request.args.get('more'), str) # Populated if AJAX request
	# Load empty page initially
	if more is None:
		return render_template('results.html')

	sid = get_sid()
	rank_key = '{}-rank'.format(sid.hex)
	args_key = '{}-args'.format(sid.hex)
	args = make_args(request.args)
	page = conv_arg(request.args.get('page'), int)
	# New client request (excluding page changes)
	if args != cache.get(args_key):
		cache.delete(rank_key) # Drinks are stale if new args
		cache.set(args_key, args)
		# print('New args!')
	ranking = cache.get(rank_key)
	if ranking is None:
		drinks = query_drink(args.dtype, args.pmin, args.pmax, args.amin, args.amax, args.base)
		# print('New drinks!')
		ranking = search_drinks(drinks, args) if len(drinks) > 0 else []
		cache.set(rank_key, ranking[:CACHE_SIZE])
	
	results = []
	ind1 = (page - 1) * PAGE_K
	ind2 = ind1 + PAGE_K
	for drink, dist in ranking[ind1:ind2]:
		results.append({
			'drink': drink.serialize,
			'dist': dist,
			'reviews': json.loads(drink.reviews) if drink.reviews is not None else []
		})

	# Populate loaded page with results
	return jsonify(
		results=results,
		count=len(ranking),
		page_number=page,
		drink_name=args.data if type(args.data) == str else None
	)

@irsystem.route('/', methods=['GET'])
def home():
	descriptors = [e.word.replace('_', ' ') for e in query_embeddings()]
	return render_template('search.html', descriptors=descriptors)
