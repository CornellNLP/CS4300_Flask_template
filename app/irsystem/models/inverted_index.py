from tokens import Tokens
from get_data import data, NUM_DOCS
from collections import Counter
import math

class InvertedIndex:
    """
    Object where obj.inv_idx is an inverted index

    ...
    Parameters
    ----------
    token_type : string
        token_type can be either 'reviews and descriptions', 
        'reviews', 'attributes', or 'descriptions'
    vector_type : string
        vector_type can be either 'tf', 'tfidf', 
        or 'binary' (no value associated with posting)
  
    Attributes
    ----------
    inv_idx: dict
        An inverted index

    Methods
    -------
    get_idfs(min_df = 15, max_df_ratio = 0.9)
        If inv_idx is tf or tfidf, return a dict of idfs
    """
    inv_idx = {}
    _vector_type = ''
    # token_type can be {'reviews and descriptions', 'reviews', 'attributes', 'descriptions'}
    def __init__(self, token_type='reviews and descriptions', vector_type = 'tf',min_df = 15, max_df_ratio= 0.9):
        assert token_type in ['reviews and descriptions', 
                              'reviews', 
                              'attributes', 
                              'descriptions']
        assert vector_type in ['binary', 'tf', 'tfidf']
        self._vector_type = vector_type

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
            self.inv_idx = inv_idx
            idfs = self.get_idfs(min_df=min_df, max_df_ratio=max_df_ratio)

            inv_idx_tfidf = {}
            for token in idfs:
                inv_idx_tfidf[token] = [(post[0], post[1] * idfs[token])for post in inv_idx[token]]

            inv_idx = inv_idx_tfidf

        self.inv_idx = inv_idx
    
    def get_idfs(self, min_df = 15, max_df_ratio= 0.9):
        assert self._vector_type in ['tf', 'tfidf']
        idfs = {}
        for token in self.inv_idx:
            n_docs_t = len(self.inv_idx[token])
            if n_docs_t >= min_df and (n_docs_t/NUM_DOCS) <= max_df_ratio:
                idfs[token] = math.log(NUM_DOCS/(1 + n_docs_t), 2)
        return idfs

    
## TEST CODE
# inv_idx = InvertedIndex(token_type='attributes', vector_type='binary')
# print(sorted(inv_idx.inv_idx.keys()))
# print(inv_idx.inv_idx)