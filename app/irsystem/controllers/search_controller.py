from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "learnddit"
net_id = "Monica Ong (myo), Eric Feng (evf23), Michelle Ip (mvi4), Zachary Brody (ztb5), Jill Wu (jw975)"

@irsystem.route('/search', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = range(5)
	# return render_template('index.html', name=project_name, netid=net_id, output_message=output_message, data=data)
