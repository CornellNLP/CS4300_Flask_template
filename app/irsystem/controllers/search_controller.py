from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Character Crafter: Turn DnD Concepts to DnD Characters"
net_id = "Vineet Parikh (vap43), Matthew Shih (ms2628), Eli Schmidt (es797), Eric Sunderland(evs37), Eric Chen(ebc48)"

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
