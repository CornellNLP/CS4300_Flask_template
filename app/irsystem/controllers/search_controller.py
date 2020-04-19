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

def rank_doc_similarity_to_word(word_in, docs, dims):
	np.random.shuffle(docs)
	vectorizer = TfidfVectorizer(stop_words = 'english')
	my_matrix = vectorizer.fit_transform([x[1] for x in docs]).transpose()
	# Most of our data is within 2 dimensions. Let's use 10
	words_compressed, _, docs_compressed = svds(my_matrix, k=dims)
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
	return closest_projects_to_word(word_in, word_to_index)


@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Play your game as: "
		p = 'app/data/classes.json'
		with open(p) as class_file:
			f = json.load(class_file)

		cdocs = [(c["class"], c["flavor"])for c in f["classes"]]
		qtokens = word_tokenize(query)
		qtokens = [word for word in qtokens if not word in stopwords.words()]
		base_ratings = dict()
		ratings_with_subclasses = dict()
		for c in f["classes"]:
			base_ratings[c["class"]]=0
		for qt in qtokens:
			rezp = rank_doc_similarity_to_word(qt, cdocs, 10)
			if(rezp!='not in vocab'):
				for rp in rezp:
					base_ratings[rp[0]]+=rp[1]
		for rating in base_ratings.values():
			if(len(qtokens)!=0):
				rating /= len(qtokens)

		for c in f["classes"]:
			for s in c["subclasses"]:
				cs_key = c["class"]+": "+s["subclass"]
				ratings_with_subclasses[cs_key]=0
			sdocs = [(c["class"]+": "+s["subclass"], s["flavor"]) for s in c["subclasses"]]
			for qt in qtokens:
				rezp = rank_doc_similarity_to_word(qt, sdocs, 1)
				if(rezp!="not in vocab"):
					for rp in rezp:
						ratings_with_subclasses[rp[0]]+=rp[1]
		if(len(qtokens)!=0):
			for k, rating in ratings_with_subclasses.items():
				base_class = k.split(":")[0] # because that's what we did
				ratings_with_subclasses[k] = rating/float(len(qtokens))+base_ratings[base_class]

		data = sorted(list(ratings_with_subclasses.items()),key = lambda x: x[1])
		print(data)
		data = list(reversed(data))[:10]
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
