from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
@import 'data_code/sent_comment_data.py';

project_name = "NJ, Sophia, Jacob, & Haley's Project"
net_id = "hcm58, sia9, ns633,"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)


@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	states = state_list
	if query not in states:
		output_message = query + ": Invalid State Name"
	else:
		sent_data = comment_sentiment
		state_sentiment = sent_data[query]
		output_message = state_sentiment

		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
