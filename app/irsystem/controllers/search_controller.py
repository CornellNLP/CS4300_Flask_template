from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import os, json
from app.irsystem.models.database_helpers import get_donations, get_tweets_by_politician

project_name = "Fundy"
net_id = "Samantha Dimmer: sed87; James Cramer: jcc393; Dan Stoyell: dms524; Isabel Siergiej: is278; Joe McAllister: jlm493"

@irsystem.route('/', methods=['GET'])
def search():
	politician_query = request.args.get('politician_name')
	free_form_query = request.args.get('free_form')
	data = []
	donation_data = []
	tweet_data = []
	if not politician_query and not free_form_query: # no input
		output_message = 'Please provide an input'
		return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, donation_data=donation_data, tweet_data=tweet_data)
	else:
		output_message = "Poltician Name: " + politician_query
		if politician_query:
			raw_donation_data = get_donations(politician_query)
			if(raw_donation_data.count() > 0):
				donation_data.append(raw_donation_data.next())
			raw_tweet_data = get_tweets_by_politician(politician_query)
			if(raw_tweet_data.count() > 0):
				tweet_data.append(raw_tweet_data.next()["tweet_text"])
		if free_form_query:
			print("Need to implement this")
		return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, donation_data=donation_data, tweet_data=tweet_data)
