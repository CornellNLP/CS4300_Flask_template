def get_rel_jokes(query, inv_idx):
    """
    Returns: dictionary mapping the joke id to its nuerator in jaccard sim

    Inputs:
        query: list of categories represented as strings
        inv_idx: dictionary mapping category to list of jokes ids that contain
            that category.
    """
    result = {}
    for cat in query:
        if cat in inv_idx:
            doc_ids = inv_idx[cat]
            for doc in doc_ids:
                if doc not in result:
                    result[doc] = 0
                result[doc] += 1
    return result

def jaccard_sim(num_dict, jokes):
    """
    Returns: a list of tuples where t[0] is the joke id and t[1] is
    the similarity measure.

    Inputs:
        num_dict - dictionary that maps joke id to its numerator in jaccard
            similarity measure.
        jokes - dictionary of jokes mapping the joke id to the joke

    """
    for doc in num_dict:
        result[doc] /= (len(set(jokes[doc]['categories']).union(set(query))))
    result = sorted(result.items(), key = lambda x : x[1], reverse = True)
    return result
