from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.comment import Comment
from nltk.tokenize import TreebankWordTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag
from collections import Counter, defaultdict
from app import app
# from app.utils import SVD
import numpy as np
import flask, os, pickle, json, math

lemmatiser = WordNetLemmatizer()
tokenizer = TreebankWordTokenizer()

@app.route('/', methods=['GET'])
def render_homepage():
  print("loading homepage")
  # print(url_for('/'))
  return render_template('index.html')

@app.route('/svd', methods=['GET'])
def get_svd():
  CLOSEST_WORDS = 2
  query = str(request.args.get('query'))
  tokens = [token for token in tokenizer.tokenize(query.lower()) if token]
  sim = []
  for token in tokens:
    sim += closest_words(token, CLOSEST_WORDS)
  return json.dumps(sim)

@app.route('/search', methods=['GET'])
def search2():
  print('searching:')
  query = str(request.args.get('query'))

  start_index = request.args.get('start_index') 
  if start_index is not None:
    print(start_index)
    start_index = int(start_index)
  else:
    start_index = 0



  # irrelevant_tokens = ['i','want','to','learn','how']
  irrelevant_tokens = []

  # we want to keep capitalization for pos-tagging in the main search method!!!
  orig_tokens = [token for token in tokenizer.tokenize(query) if token not in irrelevant_tokens]

  # these will be used for everything else
  tokens = [token for token in tokenizer.tokenize(query.lower()) if token not in irrelevant_tokens]
  tokens = expand_query(orig_tokens)

  index, tokens = build_index(tokens)
  results = index_search(tokens, orig_tokens, index, app.config['idfs'], app.config['doc_norms'], start_index)

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

def closest_words(word_in, k):
  words_compressed = app.config['words_compressed']
  word_to_index = app.config['word_to_index']
  index_to_word = app.config['index_to_word']
  if word_in not in word_to_index: return []
  sims = words_compressed.dot(words_compressed[word_to_index[word_in], :])
  asort = np.argsort(-sims)[:k + 1]
  return [(index_to_word[i], sims[i] / sims[asort[0]]) for i in asort[1:]]

def expand_query(query_tokens):
  # builds a list of tokens that are the stemmed versions of the word
  # see marcobonzanini.com/2015/01/26/stemming-lemmatisation-and-pos-tagging-with-python-and-nltk/
  CLOSEST_WORDS = 2
  addtl_tokens = set([])
  tokens_pos = pos_tag(query_tokens)

  for (token, pos_treebank) in tokens_pos:
    # get stemmed words
    pos = get_wordnet_pos(pos_treebank)
    if pos == '':
      continue
    addtl_tokens.add(lemmatiser.lemmatize(token, pos=pos))

    # use SVD to get related words
    for (word, _) in closest_words(token, CLOSEST_WORDS):
      addtl_tokens.add(word)

  # LMFAO need to do this to ensure no overlap between addtl_tokens and query_tokens
  return list(set(query_tokens).union(addtl_tokens))

def build_index(query_tokens):
  # builds a query-specfic inverted index by loading the words
  # in the query that are also in the inverted index

  tokens = query_tokens
  print tokens
  print("got index tokens:" + str(tokens))
  index = dict()
  for token in tokens:
    if str(token) in app.config["valid_words"]:
      f = open(os.getcwd() + "/app/utils/data/" + token + ".pkl","rb")
      d = pickle.load(f)
      index[token] = d
    else:
      index[token] = {}
  return index, tokens

def index_search(query_tokens, orig_tokens, index, idf, doc_norms, start_index=0):
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

  # get the parts of speech with the included sentence to help the perceptron
  base_sentence = ["I", "want", "to", "learn", "how", "to"]
  tokens_pos = pos_tag(base_sentence + orig_tokens)

  word_weights = {}

  # query expnaded words get a score of 1 by default because otherwise certain words
  # that have been expanded get too much weight I'll fix this later -eric
  for token in tokens:
    word_weights[token] = 1

  # nouns are important, want to have them in the response
  nouns = set([])

  # weigh adj/adverbs lower then verbs, which are weighed lower than nouns
  for (token, treebank_tag) in tokens_pos:
    if token in base_sentence or token in word_weights:
      continue

    # lower is necessary because we kept capitalization from the original query for POS tagging!
    token = token.lower()
    if treebank_tag.startswith('J') or treebank_tag.startswith('R'):
      word_weights[token] = 1
    elif treebank_tag.startswith('V'):
      word_weights[token] = 5
    elif treebank_tag.startswith('N'):
      word_weights[token] = 10
      nouns.add(token)
    else:
      word_weights[token] = 0

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
          (idf[token] ** 2) * query_count * word_weights[token]**2 / \
          (query_norm + 1)

  # have a score breakdown dict to display on frontend
  # first entry of breakdown is baseline cos_sim score
  # second entry is the noun score
  # third entry is the upvote score
  # fourth entry will be the token count score
  # final entry will be the final score
  score_breakdowns = {}

  #significantly reduce scores of comments without nouns in it
  noun_docs = set([])
  for token in nouns:
    noun_docs.update(set(index[token].keys()))

  for doc_id in scores.keys():
    # init the breakdown to be the base cos-sim score
    score_breakdowns[doc_id] = [scores[doc_id], 1]
    if doc_id not in noun_docs and len(noun_docs) != 0:
      scores[doc_id] *= 0.1

      # appropriately set the second entry of breakdown
      curr_score_breakdown = score_breakdowns[doc_id]
      curr_score_breakdown[1] = 0.1
      score_breakdowns[doc_id] = curr_score_breakdown

  # will map comment ids to the comment dicts
  id_to_comment = {}

  # get all comments from DB from a list of keys
  comment_objs = Comment.query.filter(Comment.comment_id.in_(scores.keys())).all()

  # create the mapping
  for comment_obj in comment_objs:
    comment_obj = cvt_Comment_to_dict(comment_obj)
    comment_body = comment_obj["body"]
    # comment_obj['summary'] = 
    id_to_comment[comment_obj["id"]] = comment_obj
    

  for doc_id in scores:
    # if comment_id is not in DB for some reason, get rid of it
    if doc_id not in id_to_comment:
      scores[doc_id] = -1
      continue

    comment = id_to_comment[doc_id]

    # factor in comment scores in the scoring
    subreddit = comment["subreddit"].lower()
    scores[doc_id] *= math.sqrt(comment["score"] * score_norm[subreddit])
    scores[doc_id] += comment["ups"] * score_norm[subreddit]
    scores[doc_id] -= comment["downs"] * score_norm[subreddit]

    # appropriately set the third entry of breakdown to be upvote score
    curr_score_breakdown = score_breakdowns[doc_id]
    curr_score_breakdown.append(comment["score"] * score_norm[subreddit])
    score_breakdowns[doc_id] = curr_score_breakdown

  # get rid of all doc ids not in the DB
  filtered_scores = {}
  for doc_id in scores:
    if (scores[doc_id] > 0):
      filtered_scores[doc_id] = scores[doc_id]

    # appropriately set the final entry to be the overall score
    curr_score_breakdown = score_breakdowns[doc_id]
    curr_score_breakdown.append(scores[doc_id])
    score_breakdowns[doc_id] = curr_score_breakdown

  sorted_list = sorted(filtered_scores.items(), key=lambda x: x[1], reverse=True)

  output = []

  for comment in sorted_list[start_index:start_index+10]:
    comment_dict = id_to_comment[str(comment[0])]
    comment_body = comment_dict["body"].encode("ascii", "ignore")
    # print(type(comment_body))
    # print(len("comment_body"))
    summary = summarizePassage(comment_body, summaryRatio=(250./len(comment_body)))
    # print(summary)
    comment_dict["summary"] = summary
    output.append([comment_dict, score_breakdowns[str(comment[0])]])

  return output

################################ HELPER FUNCTIONS ##################################

def get_reddit_comment_as_dict(id):
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
  """
  Given a comment object, convert it to a universal, unchanging dict
  to standardize representation
  """
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

# https://stackoverflow.com/questions/37939341/how-do-i-get-started-with-a-project-on-text-summarization-using-nlp
def summarizePassage(text,summaryRatio=0.5):
  from gensim.summarization import summarize
  try:
    summary = summarize(text,split=True,ratio=summaryRatio)
  except:
    print "WARNING: Gensim unable to reduce text"
    return [text]
  return "...".join(summary)
