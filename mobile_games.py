import pandas as pd
import re
import math
from collections import Counter

mgs = pd.read_csv('googleplaystore.csv')

app_categories = mgs[‘category’]
booleans = []
for cat in app_categories:
    if not re.search('GAME', cat):
        booleans.append(False)
    else:
        booleans.append(True)

Filtered = pd.Series(booleans)
game_apps = mgs[Filtered]

mgs_sets = dict()
for i in range(len(game_apps['App'])):
    key = game_apps['App'][i]
    app_type = game_apps['Type'][i]
    content = game_apps['Content Rating'][i]
    genres = game_apps['Genres'][i].split(';')
    mgs_sets[key] = set(app_type) | set(content) | set(genres)


def mgs_jaccard(app1, app2):
    A_int_B = mgs_sets[app1].intersection(mgs_sets[app2])
    A_uni_B = mgs_sets[app1].union(mgs_sets[app2])
    return len(A_int_B) / len(A_uni_B)


def mgs_jaccard_list(app):
    score_list = []
    for k in game_apps['App']:
        if k != app:
            score_list.append((x, mgs_jaccard(app, k)))
    return score_list


# compute tf-idf vectors and cossim

mg_revs = pd.read_csv('googleplaystore.csv')


def tokenize(text):
    return [x for x in re.findall(r"[a-z]+", text.lower())]


app_set = set(mg_revs['App'])
N = len(app_set)

tok_lists = dict()
for app in app_set
for j in range(len(mg_revs['App'])):
    app_name = mg_revs['App'][j]
    if app == app_name:
         review = mg_revs['Translated_Review'][j]
          tokenized_review = tokenize(review)
           if app in review_tokens:
                review_tokens[app] = review_tokens[app] + tokenized_review
            else:
                review_tokens[app] = tokenized_review

inv_idx = dict()
for app in app_set:
    tokens = tok_lists[app]
    token_set = set(tokens)
    for term in token_set:
        tf = tokens.count(term)
        tf_dict[term] = (app, tf)

idf_dict = dict()
for term in inv_idx:
    df = len(inv_idx[term])
    if df >= 50 and df / N <= 0.9:
        idf[term] = math.log2(N / (df + 1))

norms_dict = dict()
acc = 0
for term in inv_idx:
    for tup in inv_idx[term]:
        app_name = tup[0]
        tf = tup[1]
        idf = idf_dict[term]
        if term in idf:
            if app_name in norms:
                norms[app_name] += (tf * idf) ** 2
            else:
                norms[doc_idx] = (tf * idf) ** 2
for app in norms_dict:
    norms_dict[app] = math.sqrt(norms_dict[app])


def mgs_cossim_list(app):
    '''
    returns sorted list of most similar games to appid based on cosine similarity
    '''
    tf = Counter(tok_lists[app])  # dict for the number of times each word appears in all the apps 
    app_score_dict = dict()

    for token in tf:
        if token in idf_dict:
            for app_name, count in inv_idx[token]:
                if app_name in app_score_dict:
                    app_score_dict[d] += tf[token] * count * (idf_dict[token] ** 2)
                else:
                    app_score_dict[d] = tf[token] * count * (idf_dict[token] ** 2)
            
    cossim = list()

    for app_name in app_score_dict:
        if app_name != app:
            app_score_dict[app_name] = app_score_dict[app_name] / (norms_dict[app] * norms_dict[app_name])
            cossim.append((app_score_dict[app_name], app_name))

    result = sorted(cossim, key=lambda pair: (-pair[0], pair[1]))

    for app_name in app_set
        if app_name not in app_score_dict and app_name != app:
            cossim.append((0, app_name))

    return cossim 


def mgs_get_rankings(score_list):
    return sorted(score_list, key=lambda x: x[1], reverse=True)



test_app = mgs['App'][0]

print('jaccard')
jaccard_scores = mgs_jaccard_list(test_app)
output_jaccard = mgs_get_rankings(jaccard_scores)
for i in range(50):
    print(output_jaccard[i])

print('cossim')
output_cossim = steam_cossim_list(test_app)
for i in range(50):
    print(output_cossim[i])

    
