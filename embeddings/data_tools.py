import json
import numpy as np
import re
from nltk.tokenize import TreebankWordTokenizer
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

DATA_DIR = 'data/'
DESC_MAP = pd.read_csv(DATA_DIR + 'descriptor_mapping.csv').set_index('raw descriptor')
TOKENIZER = TreebankWordTokenizer()

# Import wine data and extract reviews.
def get_wine_data():
    f=open(DATA_DIR+"winemag-data-130k-v2.json", "r")
    transcripts = json.load(f)
    transcripts = transcripts[0:25000]
    return [t["description"] for t in transcripts]

# Import beer data and extract reviews.
def get_beer_data():
    transcripts = pd.read_csv(DATA_DIR+"beer_train.csv").to_numpy()
    transcripts = transcripts[0:25000]
    return [t[4] for t in transcripts]

def get_descriptor(word):
    if word in list(DESC_MAP.index):
        norm = DESC_MAP['level_3'][word]
        return norm
    else:
        return word

# Returns a list of unique types that appear in the corpus.
# @param data_list is a list of strings where each string is the review for a
# beverage and the index of the string is the index of the beverage that the
# review corresponds to.
def tokenize(data_list):
    bev_tokens = []
    descr_rgx = "[a-z]+"
    num_docs = len(data_list)
    for doc_ind in range(0, num_docs):
        tokens = set(TOKENIZER.tokenize(data_list[doc_ind].lower()))
        fil_tokens = [x for x in tokens if re.match(descr_rgx, x)]
        bev_tokens.append(fil_tokens)
    types = list(set(token for token_list in bev_tokens for token in token_list))
    return types
