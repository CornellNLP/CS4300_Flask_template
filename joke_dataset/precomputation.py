import numpy as np
from numpy import linalg as LA
import json
import math

with open("final_toks.json") as f:
    data = json.load(f)

NUM_JOKES = len(data)
print("Loaded {} jokes".format(NUM_JOKES))
print("Each joke has the following keys:")
print(data[0].keys())

def build_inverted_indices(jokes):
    result = {}
    result_cat = {}
    for joke in range(len(jokes)):
        toks = jokes[joke]['toks']
        cats = jokes[joke]['categories']
        tmp = {}
        tmp_cat = {}
        for tok in toks:
            if tok not in tmp:
                tmp[tok] = 0
            tmp[tok] += 1
        for key in tmp:
            if key not in result:
                result[key] = [(joke+1, tmp[key])]
            else:
                result[key].append((joke+1, tmp[key]))

        for cat in cats:
            if cat not in result_cat:
                result_cat[cat] = [joke+1]
            else:
                result_cat[cat].append(joke+1)
    return result, result_cat

inv_idx, inv_idx_cat = build_inverted_indices(data)

def sep_tups(inv_idx):
    result = [] 
    for i in inv_idx:
        temp = {}
        temp['term'] = i
        docs = []
        tf = []
        for t in inv_idx[i]:
            docs.append(t[0])
            tf.append(t[1])
        temp['joke_ids'] = docs
        temp['tfs'] = tf
        result.append(temp)
    return result 

new_inv_idx = sep_tups(inv_idx)

def edit_cats(inv_idex_cat):
    result = []
    for category, ls in inv_idx_cat.items():
        temp = {}
        temp['category'] = category
        temp['joke_ids'] = ls
        result.append(temp)
    return result

new_inv_idx_cat = edit_cats(inv_idx_cat)
        
with open('inv_idx_free.json', 'w') as f:
    json.dump(new_inv_idx, f, indent=4)
with open('inv_idx_cat.json', 'w') as f:
    json.dump(new_inv_idx_cat, f, indent=4)
# def compute_cat_num(jokes):
#     result = []
#     for i in range(len(jokes)):
#         result.append(len(jokes[i]['categories']))
#     return result
#
# cat_num = compute_cat_num(data)

def compute_idf(inv_idx, n_docs, min_df=10, max_df_ratio=0.90):
    idf = {}

    for word in inv_idx:
        wrd_lst = inv_idx[word]
        lst_len = len(wrd_lst)
        if lst_len >= min_df and (lst_len/n_docs) <= max_df_ratio:
            idf[word] = math.log2(n_docs/(1+lst_len))

    return idf

idf_dict = compute_idf(inv_idx, NUM_JOKES)

with open('idf_dict.json', 'w') as f:
    json.dump(idf_dict, f, indent=4)

def compute_doc_norms(inv_idx, idf_dict, n_docs):
    result = np.zeros(n_docs)

    for word in inv_idx:
        if word in idf_dict:
            curr_idf = idf_dict[word]
            for t in inv_idx[word]:
                doc = t[0]-1
                tf = t[1]
                result[doc] += math.pow(tf*curr_idf, 2)
    result = np.sqrt(result)
    return result

doc_norms_lst = compute_doc_norms(inv_idx, idf_dict, NUM_JOKES)

def add_norms(jokes, norms):
    result = [] 
    for i in range(len(jokes)):
        temp = {}
        temp['joke'] = jokes[i]['joke']
        temp['categories'] = jokes[i]['categories']
        temp['score'] = jokes[i]['score']
        temp['norm'] = norms[i]
        result.append(temp)
    return result
   
new_final = add_norms(data, doc_norms_lst)

with open('final_norm.json', 'w') as f:
    json.dump(new_final, f, indent=4)

def jaccard_sim(query, inv_idx, jokes):
    result = {}
    for cat in query:
        if cat in inv_idx:
            doc_ids = inv_idx[cat]
            for doc in doc_ids:
                if doc not in result:
                    result[doc] = 0
                result[doc] += 1
    for doc in result:
        result[doc] /= (len(set(jokes[doc]['categories']).union(set(query))))
    result = sorted(result.items(), key = lambda x : x[1], reverse = True)
    return result

jaccard = jaccard_sim(['Dad Jokes'], inv_idx_cat, data)
