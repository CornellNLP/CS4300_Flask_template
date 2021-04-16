from . import *
from app.irsystem.models.search import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Ski Resort Recommendations"
net_id = "Ava Anderson: aca76, Michael Behrens: mcb273, Cameron Haarmann: cmh332, Nicholas Mohan: nhm39, Megan Tormey: mt664"

@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    if not query:
        data = []
        output_message = ''
    else:
        output_message = "Your search: " + query
        ski_dict = load_data()
        data = search(query, ski_dict)
    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
