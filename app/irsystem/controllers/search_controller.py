from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from data_code.sent_comment_data import comment_sentiment, state_list

project_name = "NJ, Sophia, Jacob, & Haley's Project"
net_id = "hcm58, sia9, ns633, jvw6"

# @irsystem.route('/', methods=['GET'])
# def search():
# 	query = request.args.get('search')
# 	if not query:
# 		data = []
# 		output_message = ''
# 	else:
# 		output_message = "Your search: " + query
# 		data = range(5)
# 	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)


@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	states = state_list
	if query not in states:
		output_message = "Invalid State Name"
	else:
		# state_sentiment = comment_sentiment[query]
		output_message = comment_sentiment
		# for tweet in state_sentiment:


	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message)
