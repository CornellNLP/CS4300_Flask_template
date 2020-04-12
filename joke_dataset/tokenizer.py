from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from numpy import linalg as LA
import json
import math
import matplotlib.pyplot as plt
from nltk.tokenize import TreebankWordTokenizer
import re

with open("final.json") as f:
    data = json.load(f)

num_jokes = len(data)
print("Loaded {} jokes".format(num_jokes))
print("Each joke has the following keys:")
print(data[0].keys())

# n_feats = 5000
# doc_by_vocab = np.empty([len(data), n_feats])
#
# def build_vectorizer(max_features, stop_words, max_df = 0.8, min_df = 10, norm = 'l2'):
#     return TfidfVectorizer(max_features = max_features, stop_words = stop_words, max_df = 0.8, min_df = 10, norm = 'l2')
#
# tfidf_vec = build_vectorizer(n_feats, "english")
# doc_by_vocab = tfidf_vec.fit_transform([d['joke'] for d in data]).toarray()
# index_to_vocab = {i:v for i, v in enumerate(tfidf_vec.get_feature_names())}

# tokenizer = re.compile(r"[^A-z]*(?=\s)\s+", re.VERBOSE)
tokenizer = re.compile(r"[^A-z0-9]*\s+[^A-z0-9]*|\.\s*", re.VERBOSE)

def add_tokens(tokenizer, data):
    result = data

    for i in range(len(result)):
        toks = tokenizer.split(result[i]['joke'].lower() + ' ')
        result[i]['toks'] = toks[:len(toks)-1]

    return result

data = add_tokens(tokenizer, data)

with open('final_toks.json', 'w') as f:
    json.dump(data, f, indent = 4)
# def build_inverted_index():
#     result = {}
#     for i in range(len(doc_by_vocab[0])):
#         tok = index_to_vocab[i]
#         result[tok] = []
#         for j in range(len(doc_by_vocab)):
#             num = doc_by_vocab[j][i]
#             if num != 0:
#                 result[tok].append((j, doc_by_vocab[j][i]))
#     return result

# inv_idx = build_inverted_index()
# print(doc_by_vocab)
# print(tfidf_vec.get_feature_names())
