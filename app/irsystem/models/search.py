from collections import Counter
import numpy as np
from nltk.tokenize import TreebankWordTokenizer
from app.irsystem.models.document_matrix import DTMat

def get_rankings_by_query(query):
    """
    Returns a list of rankings given a query string.
    This serves as the main function that is called when a new query is made.
    """
    # Create tfidf matrix object for trail documents with 200 features
    trails_tfidf = DTMat(token_type='reviews and descriptions', features=200)

    # Create tfidf vector for query of size (1, 200)
    query_tokens = tokenize_string(query)
    features = trails_tfidf.feature_names
    idfs = trails_tfidf.inv_idx.get_idfs()
    query_tfidf_vec = tfidfize_query(query_tokens, features, idfs)

    # Calculate cosine similarity between query and all documents

    # Return the top 3 highest values
    return []

def tokenize_string(s):
    """
    Given an input string s, returns a list of tokens in the string.
    """
    tokenize = TreebankWordTokenizer().tokenize
    return tokenize(s.lower())

def tfidfize_query(q, features, idfs):
    """
    Given an input list of tokens q, returns a tfidf vector of size (1, [# of features]) representing q.
    If a term appears in q that is not in the given features, ignore it.
    """
    tfidf_vec = np.zeros(len(features))
    tf_q = { term:freq for term, freq in Counter(q).items() if term in idfs }

    for i, token in enumerate(features):
        tfidf_vec[i] = tf_q.get(token, 0) * idfs.get(token, 0)

    return tfidf_vec