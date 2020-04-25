import json
from sklearn.linear_model import LinearRegression, LogisticRegression
from mord import LogisticAT
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import make_scorer
import numpy as np
import prob_lib1 as pl
from nltk.tokenize import TreebankWordTokenizer

with open('dataset_raw.json') as f:
  data = json.load(f)

def organize(jokes):
  unscore = []
  score = []
  for i in jokes:
    if i['score']:
      score.append(i)
    else:
      unscore.append(i)
  return unscore, score

model_linear = LinearRegression()
model_1vR = LogisticRegression(multi_class = 'ovr',
    class_weight = 'balanced')
model_multi = LogisticRegression(multi_class = 'multinomial',
    solver = 'lbfgs',
    class_weight = 'balanced')
model_ordinal = LogisticAT(alpha = 0)

jokes = organize(data)[1]
target = [i['score'] for i in jokes]
jokes = [i['joke'] for i in jokes]

tokenizer = TreebankWordTokenizer()
feats, fea_to_idx = pl.get_features(jokes, tokenizer)
mtrx = pl.create_mtrx(jokes, feats, fea_to_idx, tokenizer)

MAE = make_scorer(mean_absolute_error)
folds = 5

# print(mtrx)
print('Mean absolute error: ')
MAE_linear = cross_val_score(model_linear,
  mtrx,
  target,
  cv = folds,
  scoring=MAE)
print('Linear regression: ', np.mean(MAE_linear))
MAE_ordinal = cross_val_score(model_ordinal,
    mtrx,
    target,
    cv=folds,
    scoring=MAE)
print('Ordered logistic regression: ', np.mean(MAE_ordinal))