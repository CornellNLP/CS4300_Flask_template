from collections import Counter
import numpy as np
from nltk.tokenize import TreebankWordTokenizer
from app.irsystem.models.document_matrix import DTMat
from app.irsystem.models.get_data import idx_to_trail_name

def get_rankings_by_query(query):
    """
    Returns a list of the top 3 rankings given a query string.
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
    num_trails = trails_tfidf.num_trails
    ranked_results = cosine_sim_matrix(num_trails, query_tfidf_vec, trails_tfidf.mat, cosine_sim)

    # Return the top 3 highest values
    return ranked_results[:3]

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

def cosine_sim(query, trail):
    """
    Returns cosine similarity of query and a trail document.
    """
    num = np.dot(query, trail)
    denom = (np.sqrt(np.sum(np.linalg.norm(query))) * np.sqrt(np.sum(np.linalg.norm(trail))))
                 
    return num / denom
 
def cosine_sim_matrix(num_trails, query, tfidf, sim_method = cosine_sim):
    # trails_sims = np.zeros(num_trails)
    trails_sims = [0 for _ in range(num_trails)]
 
    # for each trail document find the cosine similarity with the query
    for i in range(0, num_trails):
        trails_sims[i] = (sim_method(query, tfidf[i]), idx_to_trail_name[i])
    
    # sorted list of all cosine similarity scores of query and trail documents
    ranked_trails = sorted(trails_sims, key= lambda x: -x[0])
    return ranked_trails
