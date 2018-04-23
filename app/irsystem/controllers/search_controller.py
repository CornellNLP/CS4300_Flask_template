from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import os, json
from app.irsystem.models.database_helpers import get_donations, get_tweets_by_politician, get_votes_by_politician, get_co_occurrence, get_relevant_donations
from empath import Empath
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import TweetTokenizer
from nltk.stem import PorterStemmer
from nltk import corpus as nltkCorp
import re
import numpy as np
from sklearn.preprocessing import normalize
from scipy.sparse import *
import time

project_name = "Fundy"
net_id = "Samantha Dimmer: sed87; James Cramer: jcc393; Dan Stoyell: dms524; Isabel Siergiej: is278; Joe McAllister: jlm493"

def process_donations(donations):
	total = 0
	donations_list = []
	print("start")
	s = time.time()
	donations = list(donations)
	print("time", str(time.time() - s))
	for don in donations:
		donations_list.append(don)
		total += float(don["TransactionAmount"])
	print("Time elapsed: ", str(time.time() - s))

	return {
		"total": total,
		"sample": sorted(donations_list, key=lambda d:d["TransactionAmount"], reverse=True)[:min(len(donations_list), 10)] 
	}

def get_issue_list(issue):
	stemmer = PorterStemmer()

	words = set([stemmer.stem(w.lower()) for w in issue.split(" ")]) - set(nltkCorp.stopwords.words('english'))
	synonyms = []
	for word in words:
		for synset in nltkCorp.wordnet.synsets(word):
			for lemma in synset.lemmas()[:min(5, len(synset.lemmas()))]:
				synonyms.append(str(lemma.name()))
	final = set(synonyms) | words

	return final



def tokenizer_custom(tweet):
    token = TweetTokenizer()
    stemmer = PorterStemmer()
    #remove links
    tweet = re.sub(r"http\S+", "", tweet)
    #remove user references
    tweet = re.sub(r"@\S+", "", tweet)
    #remove phone numbers
    tweet = re.sub(r'((1-\d{3}-\d{3}-\d{4})|(\(\d{3}\) \d{3}-\d{4})|(\d{3}-\d{3}-\d{4})|(\(\d{3}\)\d{3}-\d{4}))', '', tweet)
    #remove punctuation
    tweet = re.sub(r'[^\w\s]','',tweet)
    #remove numbers
    tweet = re.sub(r"\d+", " ", tweet)
    #tokenize
    tokens = token.tokenize(tweet)
    #stem
    tokens = [stemmer.stem(token) for token in tokens]

    return tokens

#return (top n tweet indices, n top tweet scores)
def process_tweets(politician, query, n):
	tweets = get_tweets_by_politician(politician)
	vocab = json.load((open("app/irsystem/models/vocab.json", 'r')))
	query_tokens = tokenizer_custom(query)

    #check query validity before proceeding
	valid_query = False
	for token in query_tokens:
		if token in vocab:
			valid_query = True
		else:
			query_tokens.remove(token)
	if valid_query == False:
		return ([],[])

    #dot query arrays
	acc = csr_matrix(np.ones(len(vocab)))
	for token in query_tokens:
    	#build vector from postings
		postings = get_co_occurrence(token)
		vectorized = np.zeros(len(vocab))
		for post_obj in postings['postings']:
			idx = post_obj['index']
			score = post_obj['score']
			vectorized[idx] = score
		vectorized = csr_matrix(vectorized)
		vec_norm = normalize(vectorized, 'l1')
		acc = acc.multiply(vec_norm)
	arr = acc.transpose()

    #vectorize politician tweets
	just_tweets = [tweet['tweet_text'] for tweet in tweets]
	vectorizer = CountVectorizer(vocabulary = vocab, tokenizer = tokenizer_custom)
	word_counts = vectorizer.fit_transform(just_tweets)

    #determine top matches
	doc_scores = (word_counts*arr).transpose()
	doc_scores = doc_scores.todense()
	top_docs = list(np.asarray(np.argsort(-1*doc_scores)))[0][:n]
	top_scores = list(np.asarray(-1*np.sort(-1*doc_scores)))[0][:n]

    #turn tweet indices into actual tweets
	tweet_lst = []
	for tweet_idx in top_docs:
		tweet_lst.append(just_tweets[tweet_idx])

	return (tweet_lst, top_scores)


@irsystem.route('/', methods=['GET'])
def search():
	politician_query = request.args.get('politician_name')
	free_form_query = request.args.get('free_form')
	lexicon = Empath()
	data = None
	if not politician_query or not free_form_query: # no input
		output_message = 'Please provide an input'
		return render_template('search.html',
				name=project_name,
				netid=net_id,
				output_message=output_message,
				data=data,
		)
	else:
		output_message = "Politician Name: " + politician_query
		data = {
			"politician": politician_query,
			"issue": free_form_query,
			"donations": [],
			"tweets": [],
			"votes": [],
			"vote_score": 0.0
		}
		if politician_query:
			#Get empath categories for free form query
			if free_form_query:
				issues_categories = lexicon.analyze(free_form_query, normalize=True)

			t = time.time()
			
			donation_data = get_relevant_donations(politician_query, get_issue_list(free_form_query))
			print("Donations returned:", donation_data.count())

			print(time.time() - t)
			t = time.time()

			don_data = process_donations(donation_data)
			data["donations"] = don_data

			print(time.time() - t)

			# top_tweets, top_tweet_scores = process_tweets(politician_query, free_form_query, 5)
			# #return top 5 for now
			# if len(top_tweets) != 0:
			# 	for tweet in top_tweets:
			# 		data["tweets"].append(tweet)

			# raw_vote_data = get_votes_by_politician(politician_query)
			# for vote in raw_vote_data:
			# 	vote_categories = lexicon.analyze(vote["vote"]["description"], normalize=True)
			# 	intersect = False
			# 	#Determine if query and vote have similar topics
			# 	if vote_categories:
			# 		for category in vote_categories:
			# 			if vote_categories[category] > 0 and issues_categories[category] > 0:
			# 				intersect = True
			# 	#If query and vote have similar topics, add the vote to vote data
			# 	if intersect:
			# 		description = vote["vote"]["description"]
			# 		politician_vote = "Unknown"
			# 		for position in vote["vote"]["positions"]:
			# 			if position["PoliticianName"] == politician_query:
			# 				politician_vote = position["vote_position"]
			# 				break
			# 		if position["vote_position"] != "Not Voting" and position["vote_position"] != "Present":
			# 			data["votes"].append({"description":description, "vote_position":politician_vote})
			# #Do basic scoring system where score is > 0 if votes yes more often and < 0 if votes no more often
			# total_yes = 0
			# total_no = 0
			# if len(data["votes"]) > 0:
			# 	for vote in data["votes"]:
			# 		if vote["vote_position"] == "Yes":
			# 			total_yes += 1
			# 		elif vote["vote_position"] == "No":
			# 			total_no += 1
			# if total_yes > total_no:
			# 	vote_score = 2.0*total_yes/(total_yes+total_no) - 1.0
			# elif total_no > total_yes:
			# 	vote_score = 2.0*total_no/(total_yes+total_no) - 1.0
			# else:
			# 	vote_score = 0.0
			# vote_score = round(vote_score, 2)
			# data["vote_score"] = vote_score
		if free_form_query:
			pass
			#print("Need to implement this")
		return render_template('search.html',
				name=project_name,
				netid=net_id,
				output_message=output_message,
				data=data,
		)
