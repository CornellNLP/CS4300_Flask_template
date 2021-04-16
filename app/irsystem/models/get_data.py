import pprint
import json

with open('../../../scrapers/ithacatrails.json') as f:
    data = json.load(f)

def get_trail_to_idx():
    trail_to_id = {}
    for i, trail in enumerate(data):
        trail_to_id[trail] = i
    return trail_to_id

NUM_DOCS = len(data)

trail_to_idx = get_trail_to_idx()
# pprint.pprint(data['Ellis Hollow Yellow trail'])