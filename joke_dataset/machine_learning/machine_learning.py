import numpy as np
from numpy import linalg as LA
import json
import math
from sklearn.model_selection import ShuffleSplit

with open("dataset_raw.json") as f:
    data = json.load(f)

def get_toks(jokes):
    """
    Returns a list of tokens in jokes and a dictionary mapping word to its
    index in the list
    """
    result = set()

    for joke in jokes:
        result = result.union(set(joke['toks']))
    result = sorted(result)

    word_to_idx = {}
    for i in range(len(result)):
        word_to_idx[result[i]] = i

    return result, word_to_idx

def organize_data(jokes):
    """
    Returns a tuple (x, y) where x is a list of jokes that need to be scored
    and y is a list of jokes that have scores.
    """
    unscored = []
    scored = []
    for joke in jokes:
        if joke['score'] == None:
            unscored.append(joke)
        else:
            scored.append(joke)
    # sort based on the score in ascending order
    scored = sorted(scored, key = lambda i: i['score'])
    return unscored, scored

unscored, scored = organize_data(data)

funny_jokes = scored[len(scored)-500:] # label top 500 jokes as 'funny'
notfunny_jokes = scored[:750] # label bottom 750 jokes as 'not funny'

funny_classes = [1 for _ in funny_jokes] # use 1 for funny
notfunny_classes = [0 for _ in notfunny_jokes] # use 0 for not funny
all_jokes = np.array(funny_jokes + notfunny_jokes) #
all_classes = np.array(funny_classes + notfunny_classes)

num_all_jokes = len(all_jokes)

shuffle_split = ShuffleSplit(n_splits = 1, test_size=0.5, random_state=0)
train_idx, test_idx = next(iter(shuffle_split.split(all_jokes)))

jokes_train = all_jokes[train_idx]
jokes_test = all_jokes[test_idx]

classes_train = all_classes[train_idx]
classes_test = all_classes[test_idx]

tok_lst, tok_to_idx = get_toks(all_jokes)

def comp_prob_dict(jk_lst, cl_lst, tok_lst, tok_idx):
    """
    Returns a dictionary where a token is the key. It contains the following
    values:
    'one_funny': Pr[t_i == 1 | funny]
    'zero_funny': Pr[t_i == 0 | funny]
    'one_notfunny': Pr[t_i == 1 | notfunny]
    'zero_notfunny' : Pr[t_i == 0 | notfunny]
    """
    funny_mtrx = np.zeros((len(tok_lst), 2))
    notfunny_mtrx = np.zeros((len(tok_lst), 2))

    print(funny_mtrx)

    for i in range(len(jk_lst)):
        lst = jk_lst[i]['toks']
        if cl_lst[i] == 1:
            for t in tok_lst:
                if t in lst:
                    funny_mtrx[tok_idx[t]][1] += 1
                else:
                    funny_mtrx[tok_idx[t]][0] += 1
        else:
            for t in tok_lst:
                if t in lst:
                    notfunny_mtrx[tok_idx[t]][1] += 1
                else:
                    notfunny_mtrx[tok_idx[t]][0] += 1

    result = {}
    num_funny = funny_mtrx[0][0] + funny_mtrx[0][1]
    num_notfunny = notfunny_mtrx[0][0] + notfunny_mtrx[0][1]
    for t in tok_lst:
        idx = tok_idx[t]
        one_funny = funny_mtrx[idx][1]/num_funny
        zero_funny = funny_mtrx[idx][0]/num_funny
        one_notfunny = notfunny_mtrx[idx][1]/num_notfunny
        zero_notfunny = notfunny_mtrx[idx][0]/num_notfunny
        result[t] = {'one_funny': one_funny, 'zero_funny': zero_funny, 'one_notfunny': one_notfunny, 'zero_notfunny': zero_notfunny}
    return result

prob_dict = comp_prob_dict(jokes_train, classes_train, tok_lst, tok_to_idx)

# def build_inverted_index(jokes):
#     result = {}
#     for joke in range(len(jokes)):
#         toks = jokes[joke]['toks']
#         tmp = {}
#         for tok in toks:
#             if tok not in tmp:
#                 tmp[tok] = 0
#             tmp[tok] += 1
#         for key in tmp:
#             if key not in result:
#                 result[key] = [(joke, tmp[key])]
#             else:
#                 result[key].append((joke, tmp[key]))
#     return result
#
# inv_idx = build_inverted_index(data)
