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

def build_inverted_index(jokes):
    result = {}
    for joke in range(len(jokes)):
        toks = jokes[joke]['toks']
        tmp = {}
        for tok in toks:
            if tok not in tmp:
                tmp[tok] = 0
            tmp[tok] += 1
        for key in tmp:
            if key not in result:
                result[key] = [(joke, tmp[key])]
            else:
                result[key].append((joke, tmp[key]))
    return result

inv_idx = build_inverted_index(data)

def compute_idf(inv_idx, n_docs, min_df=10, max_df_ratio=0.90):
    idf = {}

    for word in inv_idx:
        wrd_lst = inv_idx[word]
        lst_len = len(wrd_lst)
        if lst_len >= min_df and (lst_len/n_docs) <= max_df_ratio:
            idf[word] = math.log2(n_docs/(1+lst_len))

    return idf

idf_dict = compute_idf(inv_idx, NUM_JOKES)

def compute_doc_norms(inv_idx, idf_dict, n_docs):
    result = np.zeros(n_docs)

    for word in inv_idx:
        if word in idf_dict:
            curr_idf = idf_dict[word]
            for t in inv_idx[word]:
                doc = t[0]
                tf = t[1]
                result[doc] += math.pow(tf*curr_idf, 2)
    result = np.sqrt(result)
    return result

doc_norms_lst = compute_doc_norms(inv_idx, idf_dict, NUM_JOKES)
