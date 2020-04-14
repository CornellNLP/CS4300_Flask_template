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

# list of toks and dictionary mapping toks to its index in [tok-lst]
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
        # additive smoothing
        one_funny = (funny_mtrx[idx][1]+1)/(num_funny + 2)
        zero_funny = (funny_mtrx[idx][0]+1)/(num_funny + 2)
        one_notfunny = (notfunny_mtrx[idx][1]+1)/(num_notfunny + 2)
        zero_notfunny = (notfunny_mtrx[idx][0]+1)/(num_notfunny + 2)
        result[t] = {'one_funny': one_funny, 'zero_funny': zero_funny, 'one_notfunny': one_notfunny, 'zero_notfunny': zero_notfunny}
    return result

prob_dict = comp_prob_dict(jokes_train, classes_train, tok_lst, tok_to_idx)

def calc_pr(jk_toks, pr_dict, tok_lst, funny):
    acc = 1
    one = None
    zero = None
    if funny:
        one = 'one_funny'
        zero = 'zero_funny'
    else:
        one = 'one_notfunny'
        zero = 'zero_notfunny'
    for tok in tok_lst:
        if tok in jk_toks:
            acc *= pr_dict[tok][one]
        else:
            acc *= pr_dict[tok][zero]
    return acc

def test_ml(pr_dict, jk_lst, cl_lst, tk_lst):
    """
    Tests on the test set and returns the correctness
    """
    num_correct = 0
    total = 0
    for jk in range(len(jk_lst)):
        cat_fun = calc_pr(jk_lst[jk]['toks'], pr_dict, tk_lst, True) * pr_funny
        cat_notfun = calc_pr(jk_lst[jk]['toks'], pr_dict, tk_lst, False) * pr_notfunny
        cat = 1 if cat_fun >= cat_notfun else 0
        if cl_lst[jk] == cat:
            num_correct += 1
        total += 1
    return num_correct/total

correctness = test_ml(prob_dict, jokes_test, classes_test, tok_lst)
print (correctness)
