from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import search_drinks, Args, Result
from app.irsystem.models.database import query_embeddings, query_drink, Drink
import json
from flask import jsonify
from uuid import uuid4

project_name = "Pick Your Poison"
net_id = """
Collin Montag (cm759),
Derek Cheng (dsc252),
DB Lee (dl654),
Dana Luong (dl697),
Ishneet Sachar (iks23)
"""

PAGE_K = 10

class CustomEncoder(json.JSONEncoder):
   def default(self, o):
      if isinstance(o, Result) or isinstance(o, Drink):
         return o.__dict__
      print('is not result')
      print(type(o))
      return json.JSONEncoder.default(self, o)

irsystem.json_encoder = CustomEncoder
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
	# indicates if async ajax request
	more = request.args.get('more')

	sid = get_sid()
	drinks_key = '{}-drinks'.format(sid.hex)
	args_key = '{}-args'.format(sid.hex)
	args = make_args(request.args)
	page = conv_arg(request.args.get('page'), int)
	drinks = cache.get(drinks_key)
	# New client request (excluding page changes)
	if args != cache.get(args_key):
		cache.set(args_key, args)
		drinks = None # Drinks are stale if new args
		# print('New args!')
	if drinks is None:
		drinks = query_drink(args.dtype, args.pmin, args.pmax, args.amin, args.amax, args.base)
		cache.set(drinks_key, drinks)
		# print('New drinks!')
	results = []
	if len(drinks) > 0:
		ranking = search_drinks(drinks, args)
		ind1 = (page - 1) * PAGE_K
		ind2 = ind1 + PAGE_K
		for i, d in ranking[ind1:ind2]:
			reviews = drinks[i].reviews
			results.append(Result(
				drink=drinks[i],
				dist=d,
				reviews=json.loads(reviews) if reviews is not None else []
			))

	if more:
		return jsonify(
			results=[{'drink': result.drink.serialize, 'dist': result.dist, 'reviews': result.reviews} for result in results],
			count=len(drinks),
			page_number=page,
			drink_name=args.data if type(args.data) == str else None,
			drink_type=args.dtype,
			base=args.base,
			descriptors=','.join(args.data) if type(args.data) == list else None,
			min_price=args.pmin,
			max_price=args.pmax,
			min_abv=args.amin,
			max_abv=args.amax
		)

	return render_template(
		'results.html',
		results=results,
		count=len(drinks),
		page_number=page,
		drink_name=args.data if type(args.data) == str else None,
		drink_type=args.dtype,
		base=args.base,
		descriptors=','.join(args.data) if type(args.data) == list else None,
		min_price=args.pmin,
		max_price=args.pmax,
		min_abv=args.amin,
		max_abv=args.amax
	)

@irsystem.route('/', methods=['GET'])
def home():
	descriptors = [e.word.replace('_', ' ') for e in query_embeddings()]
	return render_template('search.html', descriptors=descriptors)
