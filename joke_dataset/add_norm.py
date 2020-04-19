import json

with open('./final.json') as f:
    data = json.load(f)

with open('./doc_norms_lst.json') as f:
    doc_norms = json.load(f)
    
def scr(jokes, norms):
    result = jokes
    for i in range(len(jokes)):
        result[i]['norm'] = norms[i]
    return result

data = scr(data, doc_norms)

with open('./final_norm.json', 'w') as f:
    json.dump(data, f, indent = 4) 
