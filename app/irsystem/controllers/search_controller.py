from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from .json_reader import json_read
from .cosine_similarity import *

project_name = "Wine Time: Your Personal Sommelier"
net_id = "Ashley Park: ap764, Junho Kim-Lee: jk2333, Sofia Yoon: hy348, Yubin Heo: yh356"

df = json_read("app/irsystem/controllers/winemag_data_withtoks.json")
inv_ind, idf, norms = precompute(df["toks"])

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		cosine = cossim(query, inv_ind, idf, norms)
		data = compute_outputs(query, cosine, df, 10)
		output_message = "Your search: " + query
		# data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

