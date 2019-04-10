from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import pickle
import json
from nltk.tokenize import TreebankWordTokenizer
import string

project_name = "Ilan's Cool Project Template"
net_id = "Ilan Filonenko: if56"
treebank_tokenizer = TreebankWordTokenizer()
wikivoyage = {}
tf_transcripts = {}
word_id_lookup = {}
tf_idf_transcripts = {}
name_id_lookup = {}
output_message = "Hey bitches"
data = []

def tokenize(query):
	tokenized_query = treebank_tokenizer.tokenize(query.lower())
	tokenized_set = list(set([x for x in tokenized_query if x not in string.puntuation]))

def tokenize_listings(listing):
	results = ""
	eat = listing['eat']
	for x in eat:
		results+= x['description']
	sleep = listing['sleep']
	for x in sleep:
		results+= x['description']
	drink = listing['drink']
	for x in drink:
		results+= x['description']
	do = listing['do']
	for x in do:
		results+= x['description']
	see = listing['see']
	for x in see:
		results+= x['description']
	return tokenize(results)

@irsystem.route('/', methods=['GET'])

def search():
	activity = request.args.get('activities')
	likes = request.args.get('likes')
	dislikes = request.args.get('dislikes')
	nearby = request.args.get('nearby')
	returnTypes = request.args.get('Returntypes')
	resultsPerPage = request.args.get('Results_per_page')
	page = request.args.get('page')

	with open ('./data/tf.pickle', 'rb') as f:
		tf_transcripts = pickle.load(f)
	with open ('./data/tfidf.pickle', 'rb') as f:
		tf_idf_transcripts = pickle.load(f)
	with open ('./data/word_id_lookup.json') as wil_file:
		word_id_lookup = json.load(wil_file)
	with open ('./data/name_id_lookup.json') as wil_file:
		name_id_lookup = json.load(wil_file)
	with open ('./data/preprocessed_wikivoyage_notext.json') as pwn_file:
		wikivoyage = json.load(pwn_file)


	# if not activity:
	# 	isActivity =
	# else:
	# 	output_message = "Your search: " + query
	# 	data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
