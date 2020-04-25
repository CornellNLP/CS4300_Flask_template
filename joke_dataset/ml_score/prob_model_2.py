import numpy as np
from numpy import linalg as LA
import json
import math
from sklearn.model_selection import ShuffleSplit
import prob_lib1 as pl

"""
Probability model of ML based on "bag of words" approach, but only using the
top 20% common tokens in the respective categories of funny vs. not funny.

Based on custom tokenizer.
"""


with open('dataset_raw.json') as f:
    data = json.load(f)

unscored, scored = pl.organize_data(data)

funny_jokes = scored[len(scored)-500:]
notfunny_jokes = scored[:750]

funny_classes = [1 for _ in funny_jokes] # use 1 for funny
notfunny_classes = [0 for _ in notfunny_jokes] # use 0 for not funny
all_jokes = np.array(funny_jokes + notfunny_jokes) #
all_classes = np.array(funny_classes + notfunny_classes)

num_all_jokes = len(all_jokes)

shuffle_split = ShuffleSplit(n_splits = 1, test_size=0.5, random_state=25)
train_idx, test_idx = next(iter(shuffle_split.split(all_jokes)))

jokes_train = all_jokes[train_idx] # jokes to train on
jokes_test = all_jokes[test_idx] # jokes to test on

# corresponding classification for training
classes_train = all_classes[train_idx]
# corresponding classification for testing
classes_test = all_classes[test_idx]

train_size = len(classes_train)
num_funny_training = np.count_nonzero(classes_train)
num_notfunny_training = train_size - num_funny_training

pr_funny = num_funny_training/train_size # Pr[funny]
pr_notfunny = num_notfunny_training/train_size # Pr[notfunny]

def get_top_toks(jk_lst, cl_lst):
    funny_toks = {}
    notfunny_toks = {}

    for jk in range(len(jk_lst)):
        toks = jk_lst[jk]['toks']
        jk_cl = cl_lst[jk]
        if jk_cl == 1:
            for tok in toks:
                if tok not in funny_toks:
                    funny_toks[tok] = 0
                funny_toks[tok] += 1
        else:
            for tok in toks:
                if tok not in notfunny_toks:
                    notfunny_toks[tok] = 0
                notfunny_toks[tok] += 1

    result_lst = []
    tok_to_idx = {}
    num_funny = np.count_nonzero(cl_lst)
    size = len(cl_lst)

    count = 0
    for tok in funny_toks:
        if funny_toks[tok] >= 0.02 * num_funny:
            result_lst.append(tok)
            tok_to_idx[tok] = count
            count += 1
    for tok in notfunny_toks:
        if (notfunny_toks[tok] >= 0.02 * (size-num_funny)) and tok not in tok_to_idx:
            result_lst.append(tok)
            tok_to_idx[tok] = count
            count += 1
    return result_lst, tok_to_idx

tok_lst, tok_to_idx = get_top_toks(jokes_train, classes_train)

prob_dict = pl.comp_prob_dict(jokes_train, classes_train, tok_lst, tok_to_idx)

correctness = pl.test_ml(prob_dict, jokes_test, classes_test, tok_lst, pr_funny, pr_notfunny)

print(correctness)
