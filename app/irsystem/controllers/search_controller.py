from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from os.path import dirname as up
from collections import defaultdict
from nltk.tokenize import TreebankWordTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds
from sklearn.preprocessing import normalize
import scipy
import numpy as np
import math


project_name = "Character Crafter: Turn DnD Concepts to DnD Characters"
net_id = "Vineet Parikh (vap43), Matthew Shih (ms2628), Eli Schmidt (es797), Eric Sunderland(evs37), Eric Chen(ebc48)"

def index_search(query, index, idf, doc_norms, tokenizer):
	""" Search the collection of documents for the given query

    Arguments
    =========

    query: string,
        The query we are looking for.

    index: an inverted index as above

    idf: idf values precomputed as above

    doc_norms: document norms as computed above

    tokenizer: a TreebankWordTokenizer

    Returns
    =======

    results, list of tuples (score, doc_id)
        Sorted list of results such that the first element has
        the highest score, and `doc_id` points to the document
        with the highest score.

    Note:

    """

	# YOUR CODE HERE
	results = np.zeros(len(doc_norms))
	answer = []
	n_docs = len(doc_norms)
	q_tokens = tokenizer.tokenize(query)
	# Setting up query tf
	query_tf = defaultdict(int)
	for w in set(q_tokens):
		query_tf[w] = q_tokens.count(w)
	# Calculate query norms
	query_norms = 0
	terms = list(idf.keys())
	for t in terms:
		t_idf = idf[t]
		query_norms += math.pow(query_tf[t] * t_idf, 2)

	for term in q_tokens:
		if term in terms:
			for doc_num, val in index[term]:
				results[doc_num] += query_tf[term] * val * idf[term] * idf[term]

	for i in range(len(doc_norms)):
		answer.append((results[i] / (math.sqrt(query_norms) * doc_norms[i]), i))
	return sorted(answer, key=lambda x: x[0], reverse=True)

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
		    return [(docs[i][0],sims[i]/sims[ssort[0]]) for i in ssort[1:]]
		rez = closest_projects_to_word(query, word_to_index)

		print(rez)
		results = []
		for t in rez:
			results.append(rez[0])
		data = rez
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
