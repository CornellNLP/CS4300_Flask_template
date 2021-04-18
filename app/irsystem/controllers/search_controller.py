from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "COVID-19 Search Engine"
net_id = "Hogun Lee hl928, Sijin Li sl2624, Irena Gao ijg24, Doreen Gui dg497, Evian Liu yl2867"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query

		# Todo: get data from scripts
		data = [
    {
      "result": "Cinema 123 by Angelika",
      "rating": 4.4,
      "score": 81,
      "cases": 28,
      "vaccinePercentage": 61.8,
      "risk": "Green"
    },
    {
        "result": "Regal Cinemas",
        "rating": 4.5,
        "score": 70,
        "cases": 31,
        "vaccinePercentage": 52.9,
        "risk": "Green"
      },
      {
        "result": "AMC Empire 25",
        "rating": 4.1,
        "score": 65,
        "cases": 31,
        "vaccinePercentage": 52.9,
        "risk": "Green"
      }
  ]

	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



