from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import os, json
from app.irsystem.models.database_helpers import *
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
	donations = list(donations)
	position_score = 0
	for don in donations:
		don["org_data"] = get_org_data(don["DonorOrganization"])
		don["TransactionAmount"] = int(don["TransactionAmount"])
		don["org_data"]["donation_total"] = int(float(don["org_data"]["donation_total"]))
		donations_list.append(don)
		total += don["TransactionAmount"]

		position_score += float(don["org_data"]["democrat_total"]) / (float(don["org_data"]["democrat_total"])+float(don["org_data"]["republican_total"]))

	if len(donations_list) > 0:
		position_score = round(position_score/len(donations_list)*100, 2)
	else:
		position_score = 50.00

	return {
		"total": total,
		"sample": sorted(donations_list, key=lambda d:d["TransactionAmount"], reverse=True)[:min(len(donations_list), 10)],
		"score": position_score,
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


# Calculate vote score based simply on if they voted yes or no on an issue
def vote_score_yes_no(votes):
	total_yes = 0
	total_no = 0
	if len(votes) > 0:
		for vote in votes:
			if vote["vote_position"] == "Yes":
				total_yes += 1
			elif vote["vote_position"] == "No":
				total_no += 1
	if total_yes > total_no:
		vote_score = 2.0*total_yes/(total_yes+total_no) - 1.0
	elif total_no > total_yes:
		vote_score = -2.0*total_no/(total_yes+total_no)
	else:
		vote_score = 0.0
	vote_score = round(vote_score, 2)
	return vote_score

# Returns percentage of people in same party this politician voted with
def vote_score_agree_with_party(votes):
	total_agree = 0.0
	total_party_votes = 0.0
	for vote in votes:
		if vote["party"] == "R":
			for key in vote["republican"]:
				if key != "majority_position" and key != "not_voting":
					total_party_votes += vote["republican"][key]
					if key == vote["vote_position"].lower():
						total_agree += vote["republican"][key]
		elif vote["party"] == "D":
			for key in vote["democratic"]:
				if key != "majority_position" and key != "not_voting":
					total_party_votes += vote["republican"][key]
					if key == vote["vote_position"].lower():
						total_agree += vote["republican"][key]
		elif vote["party"] == "I":
			for key in vote["independent"]:
				if key != "majority_position" and key != "not_voting":
					total_party_votes += vote["independent"][key]
					if key == vote["vote_position"].lower():
						total_agree += vote["independent"][key]
		#If independent, simply return 0?
	if len(votes) == 0 or len(votes) == total_party_votes:
		score = 0
	else:
		score = round((total_agree-len(votes))/(total_party_votes-len(votes)), 2)
	return score
	
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
	vocab = json.load((open("app/irsystem/models/vocab.json", 'r')))['vocab']
	query_tokens = tokenizer_custom(query)

    #check query validity before proceeding
	for token in query_tokens:
		if token in vocab:
			valid_query = True
		else:
			query_tokens.remove(token)
	if valid_query == False:
		return ([],[])

	#dot query arrays
	query_dict = {}
	for token in query_tokens:
		postings = get_co_occurrence(token)['postings']
		for posting in postings:
			idx = posting['index']
			score = posting['score']
			word = vocab[idx]
			if word in query_dict:
				query_dict[word] *= score
			else:
				query_dict[word] = score

	#get similarity for each tweet
	sim_scores = []
	just_tweets = []
	for tweet in tweets:
		text = tweet['tweet_text']
		sentiment = tweet['sentiment']
		just_tweets.append((text, sentiment))
		tokens = tokenizer_custom(text)
		sim_score = 0.0
		for token in tokens:
			if token in query_dict:
				sim_score += query_dict[token]
		sim_scores.append(sim_score)

	sim_scores = np.array(sim_scores)

	top_scores = -1*np.sort(-1*sim_scores)[:n]
	top_docs = np.argsort(-1*sim_scores)[:n]

	final_lst = []
	total_sentiment = 0.0
	for i in range(len(top_docs)):
		idx = top_docs[i]
		final_lst.append({"tweet": just_tweets[idx][0], "sentiment": just_tweets[idx][1], "score": top_scores[i]})
		total_sentiment += just_tweets[idx][1]["compound"]

	return (final_lst, total_sentiment)

@irsystem.route('/', methods=['GET'])
def search():
	politician_query = request.args.get('politician_name')
	free_form_query = request.args.get('free_form')
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
		output_message = "Politician Name: " + politician_query + " - Issue: " + free_form_query
		data = {
			"politician": politician_query,
			"issue": free_form_query,
			"donations": [],
			"tweets": [],
			"votes": [],
			"vote_score": 0.0
		}
		if politician_query:	
			donation_data = get_relevant_donations(politician_query, get_issue_list(free_form_query))

			don_data = process_donations(donation_data)
			data["donations"] = don_data

			tweet_dict, total_sentiment = process_tweets(politician_query, free_form_query, 10)
			avg_sentiment = round(total_sentiment/10,2)
			#return top 5 for now
			if len(tweet_dict) != 0:
				data["tweets"] = {'tweet_dict': tweet_dict, 'avg_sentiment': avg_sentiment}

			raw_vote_data = get_votes_by_politician(politician_query)
			# Find all votes that have a subject that contains the issue typed in
			query_lower = free_form_query.lower()
			for vote in raw_vote_data:
				issue_in_topics = False
				relevant_topic = ""
				if "subjects" in vote["vote"].keys():
					for topic in vote["vote"]["subjects"]:
						if query_lower in topic["name"].lower():
							issue_in_topics = True
							relevant_topic = topic["name"]
							break
				#If query and vote have similar topics or if query in bill description, add the vote to vote data
				if issue_in_topics or free_form_query.lower() in vote["vote"]["description"].lower():
					description = vote["vote"]["description"]
					politician_vote = "Unknown"
					for position in vote["vote"]["positions"]:
						if position["PoliticianName"] == politician_query:
							politician_vote = position["vote_position"]
							politician_party = position["party"]
							democratic_votes = vote["vote"]["democratic"]
							republican_votes = vote["vote"]["republican"]
							independent_votes = vote["vote"]["independent"]
							break
					if position["vote_position"] != "Not Voting" and position["vote_position"] != "Present":
						data["votes"].append({"relevant_topic":relevant_topic, "description":description, "vote_position":politician_vote, "independent":independent_votes, "democratic":democratic_votes, "republican":republican_votes, "party":politician_party})
			#Do basic scoring system where score is % of time vote with party
			vote_score = vote_score_agree_with_party(data["votes"])
			data["vote_score"] = vote_score
		if free_form_query:
			pass
			#print("Need to implement this")
		return render_template('search.html',
				name=project_name,
				netid=net_id,
				output_message=output_message,
				data=data,
		)