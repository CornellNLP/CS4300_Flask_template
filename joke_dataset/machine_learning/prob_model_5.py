import numpy as np
import prob_lib1 as pl

from sklearn.model_selection import ShuffleSplit
from sklearn.naive_bayes import BernoulliNB

from sklearn.metrics import classification_report

with open('dataset_raw.json') as f:
    data = json.load(f)

unscored, scored = pl.organize_data(data)

funny_jokes = scored[len(scored)-500:] # label top 500 jokes as 'funny'
notfunny_jokes = scored[:750] # label bottom 750 jokes as 'not funny'

funny_classes = [1 for _ in funny_jokes] # use 1 for funny
notfunny_classes = [0 for _ in notfunny_jokes] # use 0 for not funny
all_jokes = np.array(funny_jokes + notfunny_jokes) #
all_classes = np.array(funny_classes + notfunny_classes)

shuffle_split = ShuffleSplit(n_splits = 1, test_size=0.5, random_state=25)
train_idx, test_idx = next(iter(shuffle_split.split(all_jokes)))

jokes_train = all_jokes[train_idx] # jokes to train on
jokes_test = all_jokes[test_idx] # jokes to test on

jokes_train = [i['joke'] for i in jokes_train]
jokes_test = [i['joke'] for i in jokes_test]

def get_features():
    """
    Features include:
    length of joke
    POS distribution
    use of Proper Nouns
    monosyllabic words
    """
    feature_lst = []
    feature_dict = {}
    feature_count = 0
