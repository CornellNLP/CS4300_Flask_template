from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import pickle
import json

project_name = "Ilan's Cool Project Template"
net_id = "Ilan Filonenko: if56"


@irsystem.route('/', methods=['GET'])
def search():
	activity = request.args.get('activities')
	likes = request.args.get('likes')
	dislikes = request.args.get('dislikes')
	nearby = request.args.get('nearby')
	returnTypes = request.args.get('Returntypes')
	resultsPerPage = request.args.get('Results_per_page')
	page = request.args.get('page')
	output_message = "Hey bitches"
	data = []


	# with open ('tf.pickle', 'rb') as f:
	# 	tf_transcripts = pickle.load(f)
	# with open ('tfidf.pickle', 'rb') as f:
	# 	tf_idf_transcripts = pickle.load(f)

	# with open ('./data/word_id_lookup.json') as wil_file:
	# 	word_id_lookup = json.load(wil_file)
	# 	for p in word_id_lookup.items():
	# 		print(p)
	# 		break
	# with open ('./data/name_id_lookup.json') as wil_file:
	# 	name_id_lookup = json.load(wil_file)
	# 	for p in name_id_lookup.items():
	# 		print(p)
	# 		break
	with open ('./data/preprocessed_wikivoyage_notext.json') as pwn_file:
		wikivoyage = json.load(pwn_file)
		for p, r in wikivoyage.items():
			# print(p)
			# print(r)
			print(r['display_title'])
			print(r['is_part_of'])
			print(r['nearby_links'])
			print(r['listings'])
			break


	
	# if not activity:
	# 	isActivity = 
	# else:
	# 	output_message = "Your search: " + query
	# 	data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



