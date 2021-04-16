from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import json

project_name = "Book Club"
net_id = "Caroline Lui: cel243, Elisabeth Finkel: esf76, Janie Walter: jjw249, Kurt Huebner: krh57, Taixiang(Max) Zeng: tz376"

# Initial route to index.html
@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = range(5)
	# return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
	return render_template('index.html', name=project_name, netid=net_id, output_message=output_message, data=data)

# Route to select.html with num_users as parameter
@irsystem.route('/select', methods=['GET'])
def select():
	query = request.args.get('num_users')
	if not query:
		return render_template('index.html')
	try:
		num_users = int(query)
	except:
		return render_template('index.html')
	return render_template('select.html', users=num_users), 200 #, name=project_name, netid=net_id, output_message=output_message, data=data)

# GET request to search for matching book names
@irsystem.route('/booknames', methods=['GET'])
def get_book_from_partial():
	partial = request.args.get('partial')
	if not partial:
		return json.dumps([])
	return json.dumps(["book1", "book2", "book3", "book4"])

# Endpoint to receive user's preferences
@irsystem.route('/result', methods=['POST'])
def get_reccs():
    print("="*50)
    print(request.data)
    print("="*50)
    req = json.loads(request.data)

    print("="*50)
    print(req)
    print("="*50)

    liked_works = req.get('liked_works')

    results = ["abc", "def"]
    return "Result (template TBD): "+str(results)
    # return render_template('result.html', results=results)

# Endpoint to redirect to result page
@irsystem.route('/result', methods=['GET'])
def get_result():
    return render_template('result.html')
