from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import search_drinks

project_name = "Pick Your Poison"
net_id = """
Collin Montag (cm759),
Derek Cheng (dsc252),
DB Lee (dl654),
Dana Luong (dl697),
Ishneet Sachar (iks23)
"""

@irsystem.route('/', methods=['GET'])
def search():
	drink_type = request.args.get('type')
	descriptors = request.args.get('descriptors')
	
	if drink_type and descriptors:
		desc_lst = [d.strip() for d in descriptors.split(',')]
		print("User searched for a {} with descriptors: {}".format(drink_type, descriptors))
		results = search_drinks(desc_lst, dtype=drink_type, k=10)
	
	# TODO change this to render results page
	return render_template('search.html')



