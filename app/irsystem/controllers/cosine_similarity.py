# Module for cosine similarity and dependent functions

from nltk.tokenize import TreebankWordTokenizer
import numpy as np
import math


def tokenizer(query):
    """
    Returns list of tokens from query.
    """
    if query is None:
        query = ""
    return TreebankWordTokenizer().tokenize(query)


def build_inverted_index(reviews):
    """
    Takes a list of token lists and returns an inverted index. A dictionary that
    maps a word to a sorted list of all the documents it appears in along with term
    frequency. The list is sorted in ascending order of doc index.
    """
    inv_ind = {}
    doc = 0
    for review in reviews:
        for word in review:
            if word in inv_ind:
                if doc in inv_ind[word]:
                    inv_ind[word][doc] += 1
                else:
                    inv_ind[word][doc] = 1
            else:
                inv_ind[word] = {doc: 1}
        doc += 1

    for word in inv_ind:
        l = [(k, v) for k, v in inv_ind[word].items()]
        l.sort(key=lambda x: x[0])
        inv_ind[word] = l

    return inv_ind


def compute_idf(inv_idx, n_docs, min_df, max_df_ratio):
    """
    Compute term IDF values from inverted index. Takes inverted index from above,
    number of docs in list (# of wines in database), minimum # of docs a term must
    occur in, maximum ratio of documents a term can occur in, and returns a
    dictionary IDF.
    """
    idf = {}
    for word in inv_idx:
        l = len(inv_idx[word])
        if l >= min_df and l/n_docs <= max_df_ratio:
            val = math.log(n_docs/(1+l), 2)
            idf[word] = val
    return idf


def compute_doc_norms(index, idf, n_docs):
    """
    Compute euclidean doc norms. Takes an inverted index and number of documents
    and returns a np array where the i'th entry is the norm of document i.
    """
    norms = np.zeros(n_docs)
    for word in index:
        if word in idf:
            for doc in index[word]:
                j = doc[0]
                tf_ij = doc[1]
                idf_i = idf[word]
                sum_term = (tf_ij * idf_i) ** 2
                norms[j] += sum_term
    norms = np.sqrt(norms)
    return norms


def cossim(query, index, idf, doc_norms):
    """
    Computes cosine similarity between query and all documents in index. Uses idf
    and doc_norms to help with precomputing values for efficiency. Returns sorted
    tuple list of (score, doc_id), ranked by score in descending order.
    """
    query = tokenizer(query.lower())
    q_tf = {}
    for word in query:
        if word in q_tf:
            q_tf[word] += 1
        else:
            q_tf[word] = 1

    q_norm = 0
    for word in query:
        if word in idf:
            q_norm += (q_tf[word] * idf[word]) ** 2
    q_norm = math.sqrt(q_norm)

    num = {}
    denom = {}
    for word in index:
        if word in query:
            if word in idf:
                for doc in index[word]:
                    doc_idx = doc[0]
                    if doc_idx not in denom:
                        denom[doc_idx] = q_norm * doc_norms[doc_idx]
                    if doc_idx in num:
                        num[doc_idx] += q_tf[word] * \
                            idf[word] * doc[1] * idf[word]
                    else:
                        num[doc_idx] = q_tf[word] * \
                            idf[word] * doc[1] * idf[word]

    output = []
    for doc in num:
        output.append((num[doc]/denom[doc], doc))
    output.sort(key=lambda x: x[1])
    output.sort(key=lambda x: x[0], reverse=True)

    return output


def precompute(reviews):
    """
    Precomputes some important values that need to be done once in the beginning
    that take a long time. The precomputed values feed directly into cossim().
    Takes in a list of list of tokens and produces an inverted index, idf dict, and
    norms dict.
    """
    inv_ind = build_inverted_index(reviews)
    n_docs = len(reviews)
    idf = compute_idf(inv_ind, n_docs, 15, .9)
    norms = compute_doc_norms(inv_ind, idf, n_docs)
    return inv_ind, idf, norms


def display(query, sim_list, reviews, num):
    """
    Takes a query, sim_list output from the cossim() function, the wine reviews df,
    and number of results to return, and prints the output to the terminal.
    Duplicate entries are caught and removed.
    """
    print("Your query: " + query)
    print("Results:")

    i = 0
    dup_list = []
    while len(dup_list) < num:
        idx = sim_list[i][1]
        title = reviews["title"][idx]
        if title not in dup_list:
            # print(title)
            dup_list.append(title)
            score = round(sim_list[i][0]*100, 2)
            desc = reviews["description"][idx]
            print("[" + str(score) + "%] " + title)
            print(desc)
            print()
        i += 1

def compute_outputs(query, sim_list, reviews, num):
    """
    Returns a list of wine results to return
    """
    result = []
    i = 0
    dup_list = []
    try:
        while len(dup_list) < num:
            idx = sim_list[i][1]
            title = reviews["title"][idx]
            if title not in dup_list:
                # print(title)
                dup_list.append(title)
                score = round(sim_list[i][0]*100, 2)
                desc = reviews["description"][idx]
                wine = "[" + str(score) + "%] " + title + desc
                result.append(wine)
            i += 1
        return result
    except:
        return ["No Results Found"]

