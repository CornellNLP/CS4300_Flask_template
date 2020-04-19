import json

with open('./inv_idx_free.json') as f:
    inv_idx = json.load(f)


def scr(inv_idx):
    result = [] 
    for i in inv_idx:
        temp = {}
        temp['term'] = i
        docs = []
        tf = []
        for t in inv_idx[i]:
            docs.append(t[0])
            tf.append(t[1])
        temp['joke_id'] = docs
        temp['tf'] = tf
        result.append(temp)
    return result 

result = scr(inv_idx)

with open('./inv_idx.json', 'w') as f:
    json.dump(result, f, indent=4)


