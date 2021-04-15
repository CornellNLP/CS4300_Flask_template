import pprint
import json

with open('../../../scrapers/ithacatrails.json') as f:
    data = json.load(f)

# pprint.pprint(data['Ellis Hollow Yellow trail'])