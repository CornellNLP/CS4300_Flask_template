from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Hiking Trail Recommender"
net_id = "Ryan Richardson: rrr225" + \
		 "Alicia Wang: axw5" + \
		 "Alicia Chen: ac2596" + \
		 "Cesar Ferreyra-Mansilla: crf85"

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



