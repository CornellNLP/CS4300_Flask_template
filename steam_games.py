import math
import numpy as np
import pandas as pd
import re

from collections import Counter

'''
GLOBAL VARIABLES
'''

# dataframe of general game info in Steam
steam_df = pd.read_csv(r'data/steam-games/steam.csv')

# dataframe of descriptions of games on Steam
steam_descriptions_df = pd.read_csv(r'data/steam-games/steam_description_data.csv')

# dictionary where key is app ID and value is set of genres
steam_sets = dict()
for i in range(len(steam_df['appid'])):
    steam_sets[steam_df['appid'][i]] = set(steam_df['genres'][i].split(';'))

# inverted indices where key is term and value is (appid, term_count_in_description)
inv_idx = dict()
# key is appid and value is list of tokens
tok_lists = dict()
for i in range(len(steam_descriptions_df['steam_appid'])):
    text = re.sub(r'<[^<>]+>', '', steam_descriptions_df['detailed_description'][i].lower())
    tok_list = re.findall(r'[a-z]+', text)
    tok_lists[steam_descriptions_df['steam_appid'][i]] = tok_list
    doc_count = dict() # contains counts for each term in document i
    for token in tok_list:
        if token in doc_count:
            doc_count[token] += 1
        else:
            doc_count[token] = 1
    for key in doc_count:
        if key in inv_idx:
            inv_idx[key].append((steam_descriptions_df['steam_appid'][i], doc_count[key]))
        else:
            inv_idx[key] = [(steam_descriptions_df['steam_appid'][i], doc_count[key])]

# dictionary where key is term and value is idf
idf = dict()
n_docs = len(steam_descriptions_df['steam_appid'])
for term in inv_idx:
    df = len(inv_idx[term])
    if df >= 50 and df / n_docs <= 0.9:
        idf[term] = math.log2(n_docs / (df + 1))

# norms[i] = the norm of description of game with appid i
norms = dict()
acc = 0
for term in inv_idx:
    for doc_count in inv_idx[term]:
        doc_idx = doc_count[0]
        if term in idf:
            if doc_idx in norms:
                norms[doc_idx] += (doc_count[1] * idf[term]) ** 2
            else:
                norms[doc_idx] = (doc_count[1] * idf[term]) ** 2
for appid in norms:
    norms[appid] = math.sqrt(norms[appid])

'''
FUNCTIONS
'''

def steam_jaccard(appid1, appid2):
    '''
    returns Jaccard similarity score between appid1 and appid2
    '''
    return len(steam_sets[appid1].intersection(steam_sets[appid2])) \
        / len(steam_sets[appid1] | steam_sets[appid2])

def steam_jaccard_list(appid):
    '''
    returns tuple list of game app IDs and Jaccard similarity scores
    '''
    score_list = list()
    for x in steam_df['appid']:
        if x != appid:
            score_list.append((x, steam_jaccard(appid, x)))
    return score_list

def steam_cossim_list(appid):
    '''
    returns sorted list of most similar games to appid based on cosine similarity
    '''
    tf = Counter(tok_lists[appid])
    doc_score_dict = dict()

    for token in tf:
        if token in idf:
            for d, c in inv_idx[token]:
                if d in doc_score_dict:
                    doc_score_dict[d] += tf[token] * c * (idf[token] ** 2)
                else:
                    doc_score_dict[d] = tf[token] * c * (idf[token] ** 2)

    result = list()

    for doc_id in doc_score_dict:
        if doc_id != appid:
            doc_score_dict[doc_id] /= norms[appid] * norms[doc_id]
            result.append((doc_score_dict[doc_id], doc_id))

    result = sorted(result, key=lambda pair: (-pair[0], pair[1]))

    for steam_appid in steam_df['appid']:
        if steam_appid not in doc_score_dict and steam_appid != appid:
            result.append((0, steam_appid))

    return result

def steam_get_rankings(score_list):
    return sorted(score_list, key=lambda x: x[1], reverse=True)

'''
TESTING
'''

print('jaccard')
output_jaccard = steam_get_rankings(steam_jaccard_list(steam_df['appid'][0]))
for i in range(50):
    print(output_jaccard[i])

print('cossim')
output_cossim = steam_cossim_list(1069460)
for i in range(50):
    print(output_cossim[i])