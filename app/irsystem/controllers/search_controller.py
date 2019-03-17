from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Get StartTED: TED Talk Recommendation System"
net_id = "Andrea Benson ab2393, Caroline Chang cdc222, Nandita Mohan nkm39, Gauri Jain gj82, Michael Rivera mr858"

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



