from nltk.tokenize import TreebankWordTokenizer
from app.jokes import *
import math

treebank_tokenizer = TreebankWordTokenizer()
def fast_cossim (query, inverted_index, tokenizer=treebank_tokenizer):
    """
        Search the collection of documents for the given query
        Inputs: 
            query: string 
            inverted_index: dictionary that matches token to a list of joke_ids
                - term
                - list of joke_ids
                - list of tfs
                - idf

        Output: list of tuples tuple = (joke, sim_score)
    """
    result = {} #dictionary mapping doc_id with sim measure
    q_list = tokenizer.tokenize(query.lower())
    q_set = set(q_list)
    
    q_norm = 0 #query norm
    inv_idx_terms = {x['term']:[(x['joke_ids'][i], x['tfs'][i]) for i in range(len(x['joke_ids']))] for x in inverted_index}
    idf = {}
    for t_dict in inverted_index:
        if t_dict['term'] in q_set and 'idf' in t_dict.keys():
            idf[t_dict['term']] = t_dict['idf']

    for q_word in q_set:
        if q_word in idf:
            tf_q = q_list.count(q_word) #how many times that word appeared in the query
            print(idf[q_word])
            print(tf_q)
            q_norm += (tf_q * idf[q_word])**2
            for tup in inv_idx_terms[q_word]:
                doc = tup[0]
                if doc not in result:
                    result[doc] = 0
                result[doc] += (tup[1] * (idf[q_word]**2) * tf_q)

    q_norm = math.sqrt(q_norm)
    for doc in result:
        norm = Joke.query.filter_by(id = doc).first().norm
        result[doc] = result[doc] / (q_norm * float(norm))

    result = sorted(result.items(), key = lambda x : (x[1], x[0]), reverse = True )
    return result

