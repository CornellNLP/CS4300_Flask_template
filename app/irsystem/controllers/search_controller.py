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

	# Retrieve rankings
	test_result1 = Result((1.0, "Cascadilla Gorge Trail - North Rim"))
	test_result2 = Result((.8, "Ellis Hollow Red trail"))
	test_result3 = Result((.5, "Stewart Park"))
	results = [test_result1, test_result2, test_result3]
	# print(results)

	if not query:
		data = []
		output_message = ''
	else:
		# Retrieve rankings
		# results = get_rankings_by_query(query)
		output_message = "Your search: " + query
		data = results

	# Render new outputs
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

