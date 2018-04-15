import os
from pymongo import MongoClient

uri = 'mongodb://fundyAdmin:Fundy4300@18.221.254.87/admin'
client = MongoClient(uri)
db = client.fundy

def get_donations(politician_name):
    return db.donations.find({"PoliticianName":politician_name})

def get_tweets_by_politician(politician_name):
    return db.tweets.find({"PoliticianName":politician_name})

def get_votes_by_politician(politician_name):
    return db.votes.find({"vote.positions.PoliticianName":politician_name})

def get_co_occurrence(word):
	return db.co_occurrence.find_one({"word":word})

# Run once to optimize querying by politician name (turns key into index)
def create_indexes():
    db.co_occurence.create_index("word")
    # db.donation.create_index("PoliticianName")
    # db.tweets.create_index("PoliticianName")
    # print(db.votes.create_index("vote.positions.PoliticianName"))
