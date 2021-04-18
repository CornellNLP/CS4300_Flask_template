from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.result import Result

project_name = "Hiking Trail Recommender"
net_id = "Ryan Richardson: rrr225" + \
		 "Alicia Wang: axw5" + \
		 "Alicia Chen: ac2596" + \
		 "Cesar Ferreyra-Mansilla: crf85"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')

	# Retrieve rankings
	test_result = Result(name="Cascadilla Gorge Trail", length=3.5)
	results = [test_result]

	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = results
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



