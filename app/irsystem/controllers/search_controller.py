from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from os.path import dirname as up
from collections import defaultdict
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds
from sklearn.preprocessing import normalize
import scipy
import numpy as np
import math


project_name = "Character Crafter: Turn DnD Concepts to DnD Characters"
net_id = "Vineet Parikh (vap43), Matthew Shih (ms2628), Eli Schmidt (es797), Eric Sunderland(evs37), Eric Chen(ebc48)"


def get_key(search_dict, val):
	for key, value in search_dict.items():
		if val == value:
			return key

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		p = 'app/data/classes.json'
		with open(p) as class_file:
			f = json.load(class_file)

		docs = [(c["class"], c["flavor"])for c in f["classes"]]
		np.random.shuffle(docs)
		vectorizer = TfidfVectorizer(stop_words = 'english')
		my_matrix = vectorizer.fit_transform([x[1] for x in docs]).transpose()
		u, s, vt = svds(my_matrix,k=11)
		# Most of our data is within 2 dimensions. Let's use 10
		words_compressed, _, docs_compressed = svds(my_matrix, k=10)
		docs_compressed = docs_compressed.transpose()
		word_to_index = vectorizer.vocabulary_
		index_to_word = {i:t for t,i in word_to_index.items()}
		words_compressed = normalize(words_compressed, axis=1)
		my_matrix_csr = normalize(scipy.sparse.csr_matrix(my_matrix))
		docs_compressed = normalize(docs_compressed, axis = 1)
		def closest_projects_to_word(word_in, word_to_index, k=15):
		    if word_in not in word_to_index: return 'not in vocab'
		    sims = docs_compressed.dot(words_compressed[word_to_index[word_in],:])
		    ssort = np.argsort(-sims)[:k+1]
		    return [(docs[i][0],sims[i]/sims[ssort[0]]) for i in ssort[0:]]

		qtokens = word_tokenize(query)
		qtokens = [word for word in qtokens if not word in stopwords.words()]
		ret = dict()
		for c in f["classes"]:
			ret[c["class"]]=0
		for qt in qtokens:
			rezp = closest_projects_to_word(qt, word_to_index)
			if(rezp!='not in vocab'):
				for rp in rezp:
					ret[rp[0]]+=rp[1]
		for rating in ret.values():
			if(len(qtokens)!=0):
				rating /= len(qtokens)
		data = sorted(list(ret.items()),key=lambda x: x[1])
		print(data)
		data = list(reversed(data))
		print(data)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
