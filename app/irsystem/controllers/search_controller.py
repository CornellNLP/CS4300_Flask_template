from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import os
from app.irsystem.models.database_helpers import testReturnAllDocuments
from app.irsystem.models.database_helpers import testInsert

project_name = "Fundy"
net_id = "Samantha Dimmer: sed87; James Cramer: jcc393; Dan Stoyell: dms524; Isabel Siergiej: is278; Joe McAllister: jlm493"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		data = []
		output_message = "Your search: " + query
		docs = testReturnAllDocuments()
		for doc in docs:
			docString = "Politician: " + doc["politician"] + ",\tTweets: "
			for tweet in doc["tweets"]:
				docString += "\"" + tweet + "\", "
			data.append(docString)
		print(data)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
