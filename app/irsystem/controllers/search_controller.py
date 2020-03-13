from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Fitness Dream Team"
net_ids = "Genghis Shyy: gs484, Henri Clarke: hxc2, Alice Hu: ath84, Michael Pinelis: mdp93, Sam Vacura: smv66"


@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    if not query:
        data = []
        output_message = ''
    else:
        output_message = "Your search: " + query
        data = range(5)
    return render_template('search.html', name=project_name, netid=net_ids, output_message=output_message, data=data)
