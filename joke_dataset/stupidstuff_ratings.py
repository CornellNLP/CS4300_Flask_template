import json

def get_score_buckets():
    data = None
    result = [0, 0, 0, 0, 0] 

    with open("stupidstuff_jokes_raw.json") as f:
        data = json.load(f)
    
    for joke in data:
        score = joke['score']
        if joke['score'] > 4:
            result[4] += 1
        elif joke['score'] > 3:
            result[3] += 1
        elif joke['score'] > 2:
            result[2] += 1
        elif joke['score'] > 1:
            result[1] += 1
        else:
            result[0] += 1
    return result 

print (get_score_buckets())

