from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import json
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import classification_report
import ml_lib as ml
from nltk.tokenize import TreebankWordTokenizer
# from sklearn.feature_extraction.text import CountVectorizer

with open('../ml_score/dataset_raw.json') as f:
  data = json.load(f)

jokes_uncat, jokes_cat = ml.organize_data(data)
categs, cat_to_idx = ml.get_categories(data)

jokes_cat = np.array(ml.assign_cat(jokes_cat, cat_to_idx))

print(len(jokes_cat))

shuffle_split = ShuffleSplit(n_splits = 1, test_size = 0.25, random_state = 1)
train_idx, test_idx = next(iter(shuffle_split.split(jokes_cat)))

jokes_train = jokes_cat[train_idx]
jokes_test = jokes_cat[test_idx]

classes_train = [i['category'] for i in jokes_train]
classes_test = [i['category'] for i in jokes_test]

jokes_train = [i['joke'] for i in jokes_train]
jokes_test = [i['joke'] for i in jokes_test]

# vectorizer = TfidfVectorizer(stop_words = 'english', max_df = 0.7, min_df = 75)
# train_mtrx = vectorizer.fit_transform(jokes_train)
# test_mtrx = vectorizer.fit_transform(jokes_test)

tokenizer = TreebankWordTokenizer()

tokens, tok_to_idx = ml.get_tokens(jokes_cat, tokenizer)

train_mtrx = ml.create_mtrx(jokes_train, tokens, tok_to_idx, tokenizer)
test_mtrx = ml.create_mtrx(jokes_test, tokens, tok_to_idx, tokenizer)

# def choosing_k(k):
#   i = 1
#   while i <= 2*k+1:
#     classifier = KNeighborsClassifier(n_neighbors = i)

#     classifier.fit(train_mtrx, classes_train)
#     predicted_classes_test = classifier.predict(test_mtrx)
#     print("Accuracy for k = {}: {:.2f}%".format(i, np.mean(predicted_classes_test == classes_test) * 100))
#     i += 2

# choosing_k(20)
classifier = KNeighborsClassifier(n_neighbors = 41)

classifier.fit(train_mtrx, classes_train)
predicted_classes_test = classifier.predict(test_mtrx)
print("Accuracy for k = {}: {:.2f}%".format(41, np.mean(predicted_classes_test == classes_test) * 100))