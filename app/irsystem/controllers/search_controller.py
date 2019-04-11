from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Get StartTED: TED Talk Recommendation System"
# net_id = "Andrea Benson ab2393, Caroline Chang cdc222, Nandita Mohan nkm39, Gauri Jain gj82, Michael Rivera mr858"
net_id = "Andrea Benson, Caroline Chang, Nandita Mohan, Gauri Jain, Michael Rivera"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
		return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

	else:
		output_message = query
		return render_template('results.html', output_message=output_message)



