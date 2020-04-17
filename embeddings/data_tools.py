import json
import string
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import pandas as pd
from gensim.parsing.preprocessing import STOPWORDS
from gensim.parsing.porter import PorterStemmer
# from sklearn.preprocessing import MultiLabelBinarizer


DATA_DIR = 'embeddings/data/'
DESC_MAP = pd.read_csv(DATA_DIR + 'descriptor_mapping.csv').set_index('raw descriptor')
STEMMER = SnowballStemmer('english')
PUNC_TABLE = str.maketrans({c: None for c in string.punctuation})
STOP_WORDS = set(stopwords.words('english'))

# Import wine data
def get_wine_data(n=None):
    transcripts = pd.read_json(DATA_DIR+"winemag-data-130k-v2.json")
    return transcripts if n is None else transcripts[0:n]
    # return [t["description"] for t in transcripts]

# Import beer data
def get_beer_data(n=None):
    transcripts = pd.read_csv(DATA_DIR+"beer_train.csv")
    return transcripts if n is None else transcripts[0:n]
    # return [t[4] for t in transcripts]

def get_descriptor(word):
    if word in list(DESC_MAP.index):
        norm = DESC_MAP['level_3'][word]
        return norm
    else:
        return word
    
# Convert raw string into a list of lowercase, stemmed, punctuation-free tokens
# TODO: Might need try/except block
def normalize(text):
    tokens = word_tokenize(text)
    res = []
    for t in tokens:
        word = str.lower(str(t))
        stem = STEMMER.stem(word)
        norm = stem.translate(PUNC_TABLE)
        if len(norm) > 1 and norm not in STOP_WORDS:
            res.append(norm)
    return res

# Return a list of unique types found in entire corpus.
def get_types(bev_tokens):
    return list(set(token for token_list in bev_tokens for token in token_list))

# Return a list of descriptors found in each wine's description where index of list
# is the document ID
# def get_doc_descriptors(data_list):
