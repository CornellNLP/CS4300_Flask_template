from . import *
from app.irsystem.models.helpers import *
from app import reddit
from nltk.tokenize import TreebankWordTokenizer
from collections import Counter
from app import app
from flask import jsonify
import flask, os, pickle

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
  index = build_index(query)
  results = index_search(query, index, app.config['idfs'], app.config['doc_norms'])
  print(results)
  comments = [get_reddit_comment(result) for result in results]
  return jsonify(comments)

def build_index(input_string):
	tokenizer = TreebankWordTokenizer()
	tokens = tokenizer.tokenize(input_string.lower())
	index = dict()
	for token in tokens:
		if token in app.config["valid_words"]:
			# print(filename)
				#print filename
			f = open(os.getcwd() + "/app/utils/data/" + token + ".pkl","rb")
			# print(f)
			d = pickle.load(f)
			# print(d)
			# print(word_id)
			index[token] = d
	return index

def get_reddit_comment(id):
  """
  Given a comment id, queries reddit API for the info and
  returns a dictionary comment containing the body, author,
  score, upvotes/downvotes, subreddit, its permalink and
  the number of gilds it has
  """
  comment = reddit.comment(id=id)
  comment_json = {}
  comment_json["body"] = comment.body
  comment_json["author"] = comment.author
  comment_json["score"] = comment.score
  comment_json["ups"] = comment.ups
  comment_json["downs"] = comment.downs
  comment_json["subreddit"] = comment.subreddit_name_prefixed
  comment_json["permalink"] = comment.permalink
  comment_json["gilded"] = comment.gilded
  return comment_json

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
