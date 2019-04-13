from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.similarity import *


project_name = "Get StartTED: TED Talk Recommendation System"
# net_id = "Andrea Benson ab2393, Caroline Chang cdc222, Nandita Mohan nkm39, Gauri Jain gj82, Michael Rivera mr858"
net_id = "Andrea Benson, Caroline Chang, Nandita Mohan, Gauri Jain, Michael Rivera"

def process_single_prompt(url): #functionality could be in a js file as well
	url_parts = url.split('=')
	prompt = url_parts[1]
	words = prompt.split('+')
	final_str = ""
	for w in words:
		final_str = final_str + " " + w
	return final_str

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
		return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

	else:
		output_message = query
		prompt1 = process_single_prompt(request.url)
		return render_template('results.html', output_message=output_message, prompt=prompt1)
