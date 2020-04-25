import numpy as np

def organize_data(jokes):
  uncat = []
  cat = []
  for joke in jokes:
    if joke['categories'] == []:
      uncat.append(joke)
    else:
      cat.append(joke)
  return uncat, cat

def get_categories(jokes):
  lst = [i for x in jokes for i in x['categories']]
  lst = set(lst)
  lst = list(lst)
  cat_to_idx = {}
  for c in range(len(lst)):
    cat_to_idx[lst[c]] = c
  return lst, cat_to_idx

def assign_cat(jokes, cat_to_idx):
  result = jokes
  for j in jokes:
    if j['categories'] != []:
      j['category'] = cat_to_idx[j['categories'][0]]
  return result

def get_tokens(jokes, tokenizer):
  features= set()
  for joke in jokes:
    toks = tokenizer.tokenize(joke['joke'].lower())
    features = features.union(set(toks))
  
  features = sorted(features)
  tok_to_idx = {}
  for i in range(len(features)):
    tok_to_idx[features[i]] = i
  
  return features, tok_to_idx

def create_mtrx(jokes, tokens, tok_to_idx, tokenizer):
  result = np.zeros((len(jokes), len(tokens)))
  for i in range(len(jokes)):
    joke_toks = tokenizer.tokenize(jokes[i].lower())
    for t in joke_toks:
      if t in tok_to_idx:
        result[i][tok_to_idx[t]] += 1
  return np.asarray(result)
