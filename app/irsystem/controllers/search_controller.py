from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import *
from app.irsystem.models.result import Result

project_name = "Hiking Trail Recommender"
net_id = "Ryan Richardson: rrr225 " + \
		 "Alicia Wang: axw5 " + \
		 "Alicia Chen: ac2596 " + \
		 "Cesar Ferreyra-Mansilla: crf85 " + \
		 "Renee Hoh: rch294 "

@irsystem.route('/', methods=['GET'])
def search():
	# Retrieve values from search query
	query = request.args.get('search')
	require_accessible = request.args.get("requireAccessible")
	require_free_entry = request.args.get("requireFreeEntry")
	require_parking = request.args.get("requireParking")

	if not query:
		data = []
		output_message = ''
	else:
		# Modify query to include toggle information
		# TODO Change how we process toggles
		if require_accessible:
			query += ' accessible'
		if require_free_entry:
			query += ' free'
		if require_parking:
			query += ' parking'

		# Retrieve rankings in the form of (sim_score, trail_name)
		rankings = get_rankings_by_query(query)
		# Convert rankings into displayable results
		results = [Result(ranking) for ranking in rankings]
		output_message = '"' + query + '"'
		data = results

	# Render new outputs
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

