from nltk.tokenize import TreebankWordTokenizer
from app.irsystem.models.document_matrix import DTMat

def get_rankings_by_query(query):
    """
    Returns a list of rankings given a query string.
    This serves as the main function that is called when a new query is made.
    """
    # Create tfidf matrix for trail documents with 200 features
    trails_tfidf_mat = DTMat(token_type='reviews and descriptions', features=200)

    # Create tfidf vector for query
    query_tokens = tokenize_string(query)

    # Calculate cosine similarity between query and all documents
    

    # Return the top 3 highest values
    return []

def tokenize_string(s):
    """
    Given an input string s, returns a list of tokens in the string.
    """
    tokenize = TreebankWordTokenizer().tokenize
    return tokenize(s.lower())
