"""
Create two thesaurus:
	one that gets top words from a category
	one that gets top words based doc term

	both using svd
"""

import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds
from sklearn.preprocessing import normalize
import matplotlib
import matplotlib.pyplot as plt


with open('./final_score.json') as f:
    data = json.load(f)


def create_thes_docs(num):
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7, min_df=75)
    mtrx = vectorizer.fit_transform([x['joke'] for x in data]).T

    words_compressed, _, docs_compressed = svds(mtrx, k=100)
    docs_compressed = docs_compressed.T

    wrd_to_idx = vectorizer.vocabulary_
    idx_to_wrd = {i: t for t, i in wrd_to_idx.items()}

    words_compressed = normalize(words_compressed, axis=1)

    wrd_to_sims = {}

    for wrd in wrd_to_idx:
        sims = words_compressed.dot(words_compressed[wrd_to_idx[wrd], :])
        asort = np.argsort(-sims)[:num+1]
        wrd_to_sims[wrd] = [idx_to_wrd[i]
                            for i in asort[1:]]

    with open('./thes_docs.json', 'w') as f:
        json.dump(wrd_to_sims, f, indent=4)


def jokes_by_cat(jokes):
    result = {}
    for joke in jokes:
        for cat in joke['categories']:
            if cat not in result:
                result[cat] = joke['joke']
            else:
                result[cat] = result[cat] + ' ' + joke['joke']

    return [result[cat] for cat in result]


def create_thes_cats(num):
    vectorizer = TfidfVectorizer(stop_words='english')
    mtrx = vectorizer.fit_transform(jokes_by_cat(data)).T

    words_compressed, _, cats_compressed = svds(mtrx, k=20)
    wrd_to_idx = vectorizer.vocabulary_
    idx_to_wrd = {i: t for t, i in wrd_to_idx.items()}

    words_compressed = normalize(words_compressed, axis=1)

    wrd_to_sims = {}

    for wrd in wrd_to_idx:
        sims = words_compressed.dot(words_compressed[wrd_to_idx[wrd], :])
        asort = np.argsort(-sims)[:num+1]
        wrd_to_sims[wrd] = [idx_to_wrd[i] for i in asort[1:]]

    with open('./thes_cats.json', 'w') as f:
        json.dump(wrd_to_sims, f, indent=4)


# print(mtrx.shape)

# u, s, v_trans = svds(mtrx, k=47)
# plt.plot(s[::-1])
# plt.show()
