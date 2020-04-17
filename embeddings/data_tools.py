import json
import numpy as np
import re
from nltk.tokenize import TreebankWordTokenizer
import pandas as pd
from gensim.parsing.preprocessing import STOPWORDS
from gensim.parsing.porter import PorterStemmer
# from sklearn.preprocessing import MultiLabelBinarizer


DATA_DIR = 'data/'
DESC_MAP = pd.read_csv(DATA_DIR + 'descriptor_mapping.csv').set_index('raw descriptor')
TOKENIZER = TreebankWordTokenizer()
# MLB = MultiLabelBinarizer()
STEMMER = PorterStemmer()

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

# Returns a list of tokens for each document where the index of the token list
# is the document ID.
def tokenize(data_list):
    bev_tokens = []
    descr_rgx = "[a-z]+"
    num_docs = len(data_list)
    # Tokenize and filter
    for doc_ind in range(0, num_docs):
        tokens = set(TOKENIZER.tokenize(data_list[doc_ind]))
        fil_tokens = []
        for x in tokens:
            match = re.match(descr_rgx, x.lower())
            if match:
                fil_tokens.append(match.group(0))
        bev_tokens.append(fil_tokens)

    # Remove stop words
    bev_tokens_fil = [[tok for tok in tok_list if tok not in STOPWORDS] for tok_list in bev_tokens]

    # Normalize tokens
    toks_stem = []
    for tok_list in bev_tokens_fil:
        toks_stem.append(list(set(STEMMER.stem_documents(tok_list))))
        
    # print(toks_stem[0:100])
    return toks_stem

# Return a list of unique types found in entire corpus.
def get_types(bev_tokens):
    return list(set(token for token_list in bev_tokens for token in token_list))

# def main():
#     tokenize(get_wine_data())
#
# main()
# Return a list of descriptors found in each wine's description where index of list
# is the document ID
# def get_doc_descriptors(data_list):
