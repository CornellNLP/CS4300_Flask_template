from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.comment import Comment
from nltk.tokenize import TreebankWordTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag
from collections import Counter, defaultdict
from app import app
import flask, os, pickle, json

lemmatiser = WordNetLemmatizer()

@app.route('/', methods=['GET'])
def render_homepage():
	print("loading homepage")
	# print(url_for('/'))
	return render_template('index.html')


@app.route('/search', methods=['GET'])
def search2():
	print('searching:')
	query = str(request.args.get('query'))

	# irrelevant_tokens = ['i','want','to','learn','how']
	irrelevant_tokens = []

	tokenizer = TreebankWordTokenizer()
	tokens = [token for token in tokenizer.tokenize(query.lower()) if token not in irrelevant_tokens]
	tokens = stem_tokens(tokens)

	index = build_index(tokens)
	results = index_search(tokens, index, app.config['idfs'], app.config['doc_norms'])

	return json.dumps(results)

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

def stem_tokens(query_tokens):
	# builds a list of tokens that are the stemmed versions of the word
	# see marcobonzanini.com/2015/01/26/stemming-lemmatisation-and-pos-tagging-with-python-and-nltk/
	tokens_pos = pos_tag(query_tokens)
	addtl_tokens = []
	for (token, pos) in tokens_pos:
		pos = get_wordnet_pos(pos)
		if pos == '':
			continue
		addtl_tokens.append(lemmatiser.lemmatize(token, pos=pos))
	print addtl_tokens
	return query_tokens + addtl_tokens

def build_index(query_tokens):
	# builds a query-specfic inverted index by loading the words
	# in the query that are also in the inverted index

	tokens = query_tokens
	print("got index tokens:" + str(tokens))
	index = dict()
	for token in tokens:
		if token in app.config["valid_words"]:
			f = open(os.getcwd() + "/app/utils/data/" + token + ".pkl","rb")
			d = pickle.load(f)
			index[token] = d
	return index

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
	score_norm = { "iwanttolearn" : 1, "explainlikeimfive" : 0 } # dont consider ELI5 anymore
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

################################ HELPER FUNCTIONS ##################################

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
	comment_dict["link_id"] = "https://www.reddit.com/" + comment.link_id[3:]
	comment_dict["permalink"] = "http://www.reddit.com/comments/" + comment.link_id[3:] + "/_/" + comment.comment_id
	comment_dict["gilded"] = comment.gilded
	return comment_dict
