from tokens import Tokens
from get_data import data, NUM_DOCS
from collections import Counter
import math
# make an inverted index where for each it can build in these ways:
# - just reviews
# - reviews and trail descriptions
# - trail attributes
# each term for keys
# and then for the postings have it be term frequency and doc names

class InvertedIndex:

    idx = {}
    # token_type can be {'reviews and descriptions', 'reviews', 'attributes', 'descriptions'}
    def __init__(self, token_type='reviews and descriptions', vector_type = 'tf', min_df = 15, max_df_ratio= 0.9):
        assert token_type in ['reviews and descriptions', 
                              'reviews', 
                              'attributes', 
                              'descriptions']
        assert vector_type in ['binary', 'tf', 'tfidf']

        tokens_per_trail = Tokens(token_type = token_type).tokens_per_trail
        inv_idx = {}
        for i in range(len(data)):
            tokens = tokens_per_trail[i]
            if vector_type == 'binary':
                tokens = set(tokens)
                for token in tokens:
                    val = inv_idx.get(token, [])
                    val.append(i)
                    inv_idx[token] = val
            else:
                tfs = Counter(tokens)
                for token in tfs:
                    val = inv_idx.get(token, [])
                    val.append((i,tfs[token]))
                    inv_idx[token] = val
        if vector_type == 'tfidf':
            idfs = {}
            for token in inv_idx:
                n_docs_t = len(inv_idx[token])
                if n_docs_t >= min_df and (n_docs_t/NUM_DOCS) <= max_df_ratio:
                    idfs[token] = math.log((NUM_DOCS/(1 + n_docs_t)), 2)
            inv_idx_tfidf = {}
            for token in inv_idx:
                n_docs_t = len(inv_idx[token])
                if n_docs_t >= min_df and (n_docs_t/NUM_DOCS) <= max_df_ratio:
                    inv_idx_tfidf[token] = math.log((NUM_DOCS/(1 + n_docs_t)), 2)
        self.inv_idx = inv_idx

inv_idx = InvertedIndex()