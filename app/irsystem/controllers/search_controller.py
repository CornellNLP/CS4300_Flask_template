from . import *
from app.irsystem.models.helpers import *
from nltk.tokenize import TreebankWordTokenizer
from collections import Counter
from app import app
import flask

@app.route('/', methods=['GET'])
def render_homepage():
	print("loading homepage")
	return render_template('search.html')


@app.route('/search', methods=['GET'])
def search2():
	print('searching:')
	# print(app.config['tf_idfs'])
	query = str(request.args.get('query'))
	print(query)
	return app.config['tf_idfs'][query.split(' ')[0]]


def index_search(query, index, idf, doc_norms):
    """ Search the collection of documents for the given query

      Arguments
      =========

      query: string,
          The query we are looking for.

      index: an inverted index as above

      idf: idf values precomputed as above

      doc_norms: document norms as computed above

      Returns
      =======

      results, list of tuples (score, doc_id)
          Sorted list of results such that the first element has
          the highest score, and `doc_id` points to the document
          with the highest score.

      """

    tokenizer = TreebankWordTokenizer()
    tokens = tokenizer.tokenize(query.lower())
    scores = np.zeros(len(doc_norms))
    counts = Counter(tokens)
    query_norm = np.linalg.norm(
        [val * idf[token] for (token, val) in counts.items() if token in idf])

    for (token, query_count) in counts.items():
        if token in idf:
            for (doc_id, doc_count) in index[token]:
                scores[doc_id] += doc_count * \
                    (idf[token] ** 2) * query_count / \
                    (doc_norms[doc_id] * query_norm + 1)

    indexed_list = [(val, i) for i, val in enumerate(scores)]
    output = sorted(indexed_list, key=lambda x: x[0], reverse=True)

    return output
