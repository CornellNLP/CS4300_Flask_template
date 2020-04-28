import json
import string
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import pandas as pd

DATA_DIR = 'embeddings/data/'
DESC_MAP = pd.read_csv(DATA_DIR + 'descriptor_mapping.csv').set_index('raw descriptor')
STEMMER = SnowballStemmer('english')
PUNC_TABLE = str.maketrans({c: None for c in string.punctuation})
STOP_WORDS = set(stopwords.words('english'))

class Headers:
    def __init__(self, name, desc, url, price=None, origin=None, abv=None, reviews=None, rating=None, base=None):
        self.name = name
        self.desc = desc
        self.price = price
        self.origin = origin
        self.abv = abv
        self.reviews = reviews
        self.rating = rating
        self.url = url
        self.base = base

STD_HDR = Headers(
    name='name',
    desc='description',
    price='price',
    origin='origin',
    abv='abv',
    reviews='reviews',
    rating='rating',
    url='url'
)

HEADERS = {
    'wine': STD_HDR,
    'beer': STD_HDR,
    'liquor': STD_HDR,
    'cocktail': Headers(
        name='name',
        desc='description',
        base='base',
        rating='rating',
        url='url'
    )
}

# Import wine training data
def get_wine_train_data(n=None):
    transcripts = pd.read_json(DATA_DIR+"winemag-data-130k-v2.json")
    return transcripts if n is None else transcripts[0:n]
    # return [t["description"] for t in transcripts]

# Import beer training data
def get_beer_train_data(n=None):
    transcripts = pd.read_csv(DATA_DIR+"beer_train.csv")
    return transcripts if n is None else transcripts[0:n]
    # return [t[4] for t in transcripts]

def get_beers():
    frames = [
        pd.read_json(DATA_DIR + "conno-beer.json"),
        pd.read_json(DATA_DIR + "shack-beer.json")
    ]
    return pd.concat(frames)

def get_wines():
    return pd.read_json(DATA_DIR + "wcom-wine.json")

def get_liquors():
    return pd.read_json(DATA_DIR + "wcom-liquor.json")

def get_cocktails():
    return pd.read_json(DATA_DIR + "spruce-cocktail.json")

def get_descriptor(word, strict):
    if word in list(DESC_MAP.index):
        norm = DESC_MAP['level_3'][word]
        return norm
    elif not strict:
        return word

def get_descriptors():
    return set(word for word in DESC_MAP['level_3'])
    
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
