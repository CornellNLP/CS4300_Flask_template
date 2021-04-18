from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import json

project_name = "Ilan's Cool Project Template"
net_id = "Ilan Filonenko: if56"

@irsystem.route('/', methods=['GET'])
def search():
  query = request.args.get('search')
  if not query:
    data = []
    output_message = ''
  else:
    output_message = "Your search: " + query

    # Todo: get data from scripts
    with open('app/static/exampleOutput.json', encoding='utf-8') as f:
      data = json.load(f)

  return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



