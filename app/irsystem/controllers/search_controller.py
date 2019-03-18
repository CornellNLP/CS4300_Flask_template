from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "DestiNationMatcher-DNM"
net_id = "Bryan Kamau: bkn7, Cynoc Bediako: cbb67, Robert Yang: ry92, Karan Newatia: kn348, Danny Yang: dzy4 "

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



