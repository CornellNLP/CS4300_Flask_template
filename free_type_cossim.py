import math
import string
import numpy as np
from nltk.tokenize import TreebankWordTokenizer

def compute_idf(inverted_idex, n_docs, min_df=10, max_df_ratio=0.95):
    idf = {}
    for word in inverted_idex:
        wrd_lst = inv_idx[word]
        lst_len = len(wrd_lst)
        if lst_len >= min_df and (lst_len/n_docs) <= max_df_ratio:
            idf[word] = math.log2(n_docs/(1+lst_len))

    return idf


def fast_cossim (query, inverted_index, idf, doc_norms, tokenizer=treebank_tokenizer):
    result = {}
    q = tokenizer.tokenize(query.lower())
    q = list( dict.fromkeys(q) )

    q_norm = 0
    q_set = set(q)
    for q_word in q_set:
        if q_word in inverted_index:
            tf_q = q.count(q_word)
            q_norm += (tf_q * idf[q_word])**2
            for tup in inverted_index[q_word]:
                doc = tup[0]
                if doc not in result:
                    result[doc] = 0
                result[doc] += (tup[1] * (idf[q_word]**2) * tf_q)

    q_norm = math.sqrt(q_norm)
    for doc in result:
        result[doc] = result[doc] / (q_norm * doc_norms[doc])

    result = sorted(result.items(), key = lambda x : (x[1], x[0]), reverse = True )
    return [tup[::-1] for tup in result]
