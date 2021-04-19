import pprint
import json

with open('ithacatrails.json') as f:
    data = json.load(f)

def get_trail_to_idx():
    trail_to_id = {}
    for i, trail in enumerate(data):
        trail_to_id[trail] = i
    return trail_to_id

def get_idx_to_trail_name(trail_to_idx_dict):
    return {value:key for key, value in trail_to_idx_dict.items()}

NUM_DOCS = len(data)

trail_to_idx = get_trail_to_idx()
idx_to_trail_name = get_idx_to_trail_name(trail_to_idx)