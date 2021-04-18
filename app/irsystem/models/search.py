import math
import json
from collections import defaultdict
def cosine_similarity(joined_queries, inverted_index, tf_idf_vectors):
    """Returns a list of work ids ranked by similarity to a query. Does not use formal cosine similarity due to the omission of normalizing by the doc norm. 

    Arguments
    =========

    joined_queries: dict,
        A dictionary representation of the joined individual queries

    inverted_index: dict,
        A dictionary mapping terms to dictionaries mapping work ids to term frequencies
    
    tf_idf_vectors: dict,
        A dictionary mapping work ids to dictionaries mapping terms to precomputed tf-idf values. Also contains a "NORM" key/value pair for each work representing precomputed doc norms.

    Returns
    ======
    ranked_results: list of size len(tf_idf_vectors)
        ranked_results[i] = work id of the i'th most relevant work
    """
    num_works = len(tf_idf_vectors)
    cosine_similarity = defaultdict(float)
    ranked_results = []
    for term, tf_idf in joined_queries.items():
        df = len(inverted_index[term])
        for work, tf in inverted_index[term].items():
            #Calculating the numerator (dot product) of cosine similarity here.
            cosine_similarity[work] += tf*math.log2(num_works/(1+df))*tf_idf
    
    #We aren't computing "true" cosine similarity, just relative rankings, hence the lack of a query norm term
    cosine = []
    for work, value in cosine_similarity.items():
        cosine.append((work,value/tf_idf_vectors[work]["NORM"]))

    cosine.sort(key = lambda x: x[1], reverse=True)
    ranked_results = [result[0] for result in cosine]
    return ranked_results


def combine_queries(work_ids, tf_idf_vectors):
    """Returns a JSON string of the top 10 most similar books to a given set of input queries

    Arguments
    =========

    work_ids: list,
        A list of works in the query
        
    tf_idf_vectors: dict,
        A dictionary mapping work ids to dictionaries mapping terms to precomputed tf-idf values. Also contains a "NORM" key/value pair for each work representing precomputed doc norms.
    Returns
    ======
    query: dict mapping terms to tf-idf values
    """
    query = defaultdict(float)
    for work in work_ids:
        for term in tf_idf_vectors[work].keys():
            if term != "NORM":
                query[term] += tf_idf_vectors[work][term]/tf_idf_vectors[work]["NORM"]
    return(dict(query))


def get_doc_rankings(work_ids, tf_idf_vectors, inverted_index, book_info):
    """Returns a dictionary of terms and tf-idf values representing the combined result of individual queries

    Arguments
    =========

    work_ids: list,
        A list of works in the query

    tf_idf_vectors: dict,
        A dictionary mapping work ids to dictionaries mapping terms to precomputed tf-idf values. Also contains a "NORM" key/value pair for each work representing precomputed doc norms.

    inverted_index: dict,
        A dictionary mapping terms to dictionaries mapping work ids to term frequencies

    book_info: dict,
        A dictionary mapping work ids to dictionaries with various book metadata.
    Returns
    ======
    results_list: A JSON-formatted list of dictionaries containing K/V pairs for title, author, ranking, book_url, image_url, and description.
    """
    combined_queries = combine_queries(work_ids, tf_idf_vectors)
    ranked_results = cosine_similarity(combined_queries, inverted_index, tf_idf_vectors)
    #Removing the query books from the rankings
    corrected_results = []
    for work in ranked_results:
        if work not in work_ids:
            corrected_results.append(work)
    
    results_list = []
    for i, work in enumerate(corrected_results[:10]):
        work_data = book_info[work]
        rankings_data_dict = {
            "title":work_data["title"],
            "author":work_data["author_names"],
            "ranking":i,
            "book_url":work_data["url"],
            "image_url":work_data["image"],
            "description":work_data["description"]
        }
        results_list.append(rankings_data_dict)
    return json.dumps(results_list)