from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
# from scripts.transcript_similarity import *
from scripts.backend_script import *

project_name = "Stream On"
net_id = "Divya Damodaran: dd492, Riya Jaggi: rj356, Siddhi Chordia: sc2538, Sidharth Vadduri: sv352, Kendall Lane: kal255"


@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    if not query:
        data = []
        output_message = ''
    else:
        output_message = "Your search: " + query
        data = jaccardRanking(query, 3)

    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
