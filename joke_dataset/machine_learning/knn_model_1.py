from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import prob_lib1 as pl
import nltk
from nltk.tokenize import TreebankWordTokenizer
from sklearn.model_selection import ShuffleSplit
import json
from sklearn.metrics import classification_report

with open('dataset_raw.json') as f:
    data = json.load(f)

unscored, scored = pl.organize_data(data)

funny_jokes = scored[len(scored)-500:] # label top 500 jokes as 'funny'
notfunny_jokes = scored[:750] # label bottom 750 jokes as 'not funny'

tokenizer = TreebankWordTokenizer()

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

# corresponding classification for training
classes_train = all_classes[train_idx]
# corresponding classification for testing
classes_test = all_classes[test_idx]

feas, word_to_idx = pl.get_features(jokes_train, tokenizer)

mtrx_train = pl.create_mtrx(jokes_train, feas, word_to_idx, tokenizer)
mtrx_test = pl.create_mtrx(jokes_test, feas, word_to_idx, tokenizer)

def choosing_k(k):
  i = 1
  while i <= 2*k+1:
    classifier = KNeighborsClassifier(n_neighbors = i)

    classifier.fit(mtrx_train, classes_train)

    predicted_classes_test = classifier.predict(mtrx_test)

    print(classifier.predict_proba(mtrx_test))
    print("Accuracy for k = {}: {:.2f}%".format(i, np.mean(predicted_classes_test == classes_test) * 100))
    i += 2

choosing_k(20)

