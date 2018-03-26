import os
from pymongo import MongoClient

uri = os.environ['DATABASE_URL']
client = MongoClient(uri)
db = client.fundy

def testInsert():
    result = db.test.insert_one(
    {
        "politician": "Hilary Clinton",
        "donors": [{"Planned Parenthood": 210000}],
        "tweets": ["Some random tweet"]
    }
)

def testReturnAllDocuments():
    return db.test.find()
