from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.comment import Comment
from nltk.tokenize import TreebankWordTokenizer
from collections import Counter, defaultdict
from app import app
import flask, os, pickle, json

@app.route('/', methods=['GET'])
def render_homepage():
	print("loading homepage")
	# print(url_for('/'))
	return render_template('index.html')


@app.route('/search', methods=['GET'])
def search2():
	print('searching:')
	# print(app.config['tf_idfs'])
	query = str(request.args.get('query'))
	# print(query)


	irrelevant_tokens = ['i','want','to','lean','how']
	tokenizer = TreebankWordTokenizer()
	tokens = [token for token in tokenizer.tokenize(query.lower()) if token not in irrelevant_tokens]
	# print(query)
	# print(tokens)

	index = build_index(tokens)
	results = index_search(tokens, index, app.config['idfs'], app.config['doc_norms'])
	# test = get_reddit_comment_as_dict(results[0])
	# print(test)
	# print(results)

	return json.dumps(results)

def build_index(query_tokens):
	tokens = query_tokens
	print("got index tokens:" + str(tokens))
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

def get_reddit_comment_as_dict(id):
	print("ID: " + str(id))
	"""
	Given a comment id, queries reddit API for the info and
	returns a json comment containing the body, author,
	score, upvotes/downvotes, subreddit, its permalink and
	the number of gilds it has
	"""
	comment = Comment.query.filter_by(comment_id=id).first()
	if comment is None:
		return None
	return cvt_Comment_to_dict(comment)

def cvt_Comment_to_dict(comment):
	comment_dict = {}
	comment_dict["id"] = comment.comment_id
	comment_dict["body"] = comment.body
	comment_dict["author"] = comment.author
	comment_dict["score"] = comment.score
	comment_dict["ups"] = comment.upvotes
	comment_dict["downs"] = comment.downvotes
	comment_dict["subreddit"] = comment.subreddit
	comment_dict["permalink"] = "t1_" + comment.comment_id
	comment_dict["gilded"] = comment.gilded
	comment_dict["link_id"] = comment.link_id
	return comment_dict

def index_search(query_tokens, index, idf, doc_norms):
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
	score_norm = { "iwanttolearn" : 75, "explainlikeimfive" : 0.25 } # arbitrary score
	tokens = query_tokens
	print("Got tokens: " + str(tokens))

	# regular cos-sim without doc_normalization
	scores = defaultdict(int)
	counts = Counter(tokens)
	query_norm = np.linalg.norm(
		[val * idf[token] for (token, val) in counts.items() if token in idf])

	for (token, query_count) in counts.items():
		if token in idf and token in index:
			for (doc_id, doc_count) in index[token].items():
				scores[doc_id] += doc_count * \
					(idf[token] ** 2) * query_count / \
					(query_norm + 1)

	# will map comment ids to the comment dicts
	id_to_comment = {}

	# get all comments from DB from a list of keys
	comment_objs = Comment.query.filter(Comment.comment_id.in_(scores.keys())).all()

	# create the mapping
	for comment_obj in comment_objs:
		comment_obj = cvt_Comment_to_dict(comment_obj)
		id_to_comment[comment_obj["id"]] = comment_obj

	# factor in comment scores in the scoring
	for doc_id in scores:
		# if comment_id is not in DB for some reason, get rid of it
		if doc_id not in id_to_comment:
			scores[doc_id] = -1
			continue

		comment = id_to_comment[doc_id]

		subreddit = comment["subreddit"].lower()
		scores[doc_id] *= comment["score"] * score_norm[subreddit]
		scores[doc_id] += comment["ups"] * score_norm[subreddit]
		scores[doc_id] -= comment["downs"] * score_norm[subreddit]

	# get rid of all doc ids not in the DB
	filtered_scores = {}
	for doc_id in scores:
		if (scores[doc_id] > 0):
			filtered_scores[doc_id] = scores[doc_id]

	output = sorted(filtered_scores.items(), key=lambda x: x[1], reverse=True)[:20]

	return [id_to_comment[str(comment[0])] for comment in output]
