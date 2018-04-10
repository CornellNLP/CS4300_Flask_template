import os
from pymongo import MongoClient

uri = os.environ['DATABASE_URL']
client = MongoClient(uri)
db = client.fundy

def get_donations(politician_name):
    return db.donations.find({"PoliticianName":politician_name})

def get_tweets_by_politician(politician_name):
    return db.tweets.find({"PoliticianName":politician_name})

def get_votes_by_politician(politician_name):
    return db.votes.find({"vote.positions.PoliticianName":politician_name})

# Run once to optimize querying by politician name (turns key into index)
def create_indexes():
    db.donations.create_index("PoliticianName")
    db.tweets.create_index("PoliticianName")
    print(db.votes.create_index("vote.positions.PoliticianName"))
