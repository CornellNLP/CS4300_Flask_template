from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import os, json
from app.irsystem.models.database_helpers import get_donations, get_tweets_by_politician, get_votes_by_politician
from empath import Empath

project_name = "Fundy"
net_id = "Samantha Dimmer: sed87; James Cramer: jcc393; Dan Stoyell: dms524; Isabel Siergiej: is278; Joe McAllister: jlm493"

@irsystem.route('/', methods=['GET'])
def search():
	politician_query = request.args.get('politician_name')
	free_form_query = request.args.get('free_form')
	lexicon = Empath()
	data = []
	donation_data = []
	tweet_data = []
	vote_data = []
	if not politician_query or not free_form_query: # no input
		output_message = 'Please provide a poltician name and issue'
		return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, donation_data=donation_data, tweet_data=tweet_data, vote_data=vote_data)
	else:
		output_message = "Poltician Name: " + politician_query
		if politician_query:
			#Get empath categories for free form query
			if free_form_query:
				issues_categories = lexicon.analyze(free_form_query, normalize=True)
			raw_donation_data = get_donations(politician_query)
			if(raw_donation_data.count() > 0):
				donation_data.append(raw_donation_data.next())
			raw_tweet_data = get_tweets_by_politician(politician_query)
			if(raw_tweet_data.count() > 0):
				tweet_data.append(raw_tweet_data.next()["tweet_text"])
			raw_vote_data = get_votes_by_politician(politician_query)
			for vote in raw_vote_data:
				vote_categories = lexicon.analyze(vote["vote"]["description"], normalize=True)
				intersect = False
				#Determine if query and vote have similar topics
				for category in vote_categories:
					if vote_categories[category] > 0 and issues_categories[category] > 0:
						intersect = True
				#If query and vote have similar topics, add the vote to vote data
				if intersect:
					description = vote["vote"]["description"]
					politician_vote = "Unknown"
					for position in vote["vote"]["positions"]:
						if position["PoliticianName"] == politician_query:
							politician_vote = position["vote_position"]
							break
					vote_data.append({"description":description, "vote_position":politician_vote})
		if free_form_query:
			print("Need to implement this")
		return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, donation_data=donation_data, tweet_data=tweet_data, vote_data=vote_data)
