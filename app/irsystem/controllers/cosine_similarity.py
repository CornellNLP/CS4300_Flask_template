# Module for cosine similarity and dependent functions

import math
import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords

nltk.download('stopwords')

stopwords = set(stopwords.words('english'))


def tokenizer(query):
    """
    Returns list of tokens from query.
    """
    if query is None:
        query = ""
    return TreebankWordTokenizer().tokenize(query)


def tokenizer_personality_data(json):
    """
    Returns a list of tokenized personality_descriptions
    """
    result = []
    for count, description in enumerate(json['personality_description']):
        tokenized = TreebankWordTokenizer().tokenize(description)
        output = [word for word in tokenized if word not in stopwords]
        result.append(output)
    return result


def tokenizer_personality_variety(json):
    """
    Returns a dictionary where the key is the string index of the personality
    data (i.e. first data is index 0, so string index is "0") and the value is 
    a list of tokenized words of the variety
    """
    result = dict()
    for count, variety in enumerate(json['variety']):
        result[count] = TreebankWordTokenizer().tokenize(variety)
    return result


def flat_tokenizer_personality_variety(json):
    """
    Returns a list of the tokenized variety types in personality-wine data
    """
    result = []
    for variety in json['variety']:
        tokenized = TreebankWordTokenizer().tokenize(variety)
        result.extend(tokenized)
    return result


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
        if l >= min_df and l / n_docs <= max_df_ratio:
            val = math.log(n_docs / (1 + l), 2)
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
                sum_term = (tf_ij * idf_i)**2
                norms[j] += sum_term
    norms = np.sqrt(norms)
    return norms


def cossim(query, index, idf, doc_norms):
    """
    Computes cosine similarity between query and all documents in index. Uses
    idf and doc_norms to help with precomputing values for efficiency. Returns
    sorted tuple list of (score, doc_id), ranked by score in descending order.
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
            q_norm += (q_tf[word] * idf[word])**2
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
        output.append((num[doc] / denom[doc], doc))
    output.sort(key=lambda x: x[1])
    output.sort(key=lambda x: x[0], reverse=True)

    return output


def cossim_dict(query, index, idf, doc_norms):
    """
    Computes cosine similarity between query and all documents in index. Uses
    idf and doc_norms to help with precomputing values for efficiency. Returns
    a dictionary where key is the [doc_id] and value is the score.
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
            q_norm += (q_tf[word] * idf[word])**2
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

    output = dict()
    for doc in num:
        output[doc] = num[doc] / denom[doc]
    return output


def total_score(dict1, dict2):
    """
    Returns a sorted list of (score, doc_id) ranked by score in descending order
    where score is the total score between dict1, dict2, dict3

    [dict#] is a dictionary where key is [doc_id] and value is [score]
    """
    result_dict = dict()
    all_data = [dict1, dict2]
    for dictionary in all_data:
        for key, value in dictionary.items():
            if key not in result_dict:
                result_dict[key] = 0
            result_dict[key] += value

    result = []
    for key, value in result_dict.items():
        result.append((value, key))
    result.sort(key=lambda x: x[1])
    result.sort(key=lambda x: x[0], reverse=True)
    return result


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


def precompute_personality(reviews):
    """
    Precomputes for personality dataset
    """
    inv_ind = build_inverted_index(reviews)
    n_docs = len(reviews)
    idf = compute_idf(inv_ind, n_docs, 0, .5)
    norms = compute_doc_norms(inv_ind, idf, n_docs)
    return inv_ind, idf, norms


def display(query, wine_scores, sim_list, reviews, num, max_price):
    """
    Takes a query, wine_scores, sim_list output from the cossim() function, the
    wine reviews df, number of results to return, and maximum price (string) 
    and prints the output to the terminal. Duplicate entries are caught and 
    removed. Only varieties of the top type according to wine_scores are printed.
    """
    print("Based on your responses, we believe these particular " +
          wine_scores[0][1] + "s will fit your taste and preference:")
    print()

    i = 0
    counter = 1
    dup_list = []
    while len(dup_list) < num:
        idx = sim_list[i][1]
        variety = reviews["variety"][idx]
        title = reviews["title"][idx]
        price = reviews["price"][idx]
        if variety == wine_scores[0][1] and price <= float(max_price):
            if title not in dup_list:
                dup_list.append(title)
                #score = round(sim_list[i][0]*100, 1)
                desc = reviews["description"][idx]
                price = reviews["price"][idx]
                #print("[" + str(score) + "%] " + title)
                print(str(counter) + ". " + title)
                print(desc)
                print("The price of this wine is: $", price)
                print()
                counter += 1
        i += 1


def display_personality(query, sim_list, reviews):
    """
    Displays the personality - wine variety match 
    """
    print("Based on personality...")
    print("You are a " + str(round(100 * sim_list[0][0], 1)) +
          "% match with " + sim_list[0][1] + "!")
    print()

    # build inverted dict
    inv_dict = {}
    for i in range(len(reviews["variety"])):
        inv_dict[reviews["variety"][i]] = i

    i = 0
    dup_list = []
    while len(dup_list) < 3:
        title = sim_list[i][1]
        dup_list.append(title)
        score = round(sim_list[i][0] * 100, 1)
        desc = reviews["personality_description"][inv_dict[title]]
        print("[" + str(score) + "%] " + title)
        print(desc)
        print()
        i += 1


def compute_wine(query, wine_scores, sim_list, reviews, num, max_price):
    """ 
    Takes a query, wine_scores, sim_list output from the cossim() function, the
    wine reviews df, and number of results to return, and prints the output to
    the terminal. Duplicate entries are caught and removed. Only varieties of
    the top type according to wine_scores are printed.
    """
    result = []
    result.append("Based on your responses, we believe these particular " +
                  wine_scores[0][1] + "s will fit your taste:")

    # i = 0
    # counter = 1
    # dup_list = []
    # while len(dup_list) < num and i < len(sim_list):
    #     idx = sim_list[i][1]
    #     variety = reviews["variety"][idx]
    #     title = reviews["title"][idx]
    #     if variety == wine_scores[0][1]:
    #         if title not in dup_list:
    #             dup_list.append(title)
    #             #score = round(sim_list[i][0]*100, 1)
    #             desc = reviews["description"][idx]
    #             #print("[" + str(score) + "%] " + title)
    #             result.append(str(counter) + ". " + title)
    #             result.append(desc)
    #             counter += 1
    #     i += 1
    # return result

    i = 0
    counter = 1
    dup_list = []
    while len(dup_list) < num and i < len(sim_list):
        idx = sim_list[i][1]
        variety = reviews["variety"][idx]
        title = reviews["title"][idx]
        price = reviews["price"][idx]
        if variety == wine_scores[0][1] and price <= float(max_price):
            if title not in dup_list:
                dup_list.append(title)
                #score = round(sim_list[i][0]*100, 1)
                desc = reviews["description"][idx]
                price = reviews["price"][idx]
                #print("[" + str(score) + "%] " + title)
                result.append(str(counter) + ". " + title)
                result.append(desc + " The price of this wine is $" +
                              str(int(price)))
                counter += 1
        i += 1
    return result


def compute_personality(query, sim_list, reviews):
    """
    Displays the personality - wine variety match 
    """
    result = []
    result.append("Based on personality...")
    result.append("You are a " + str(round(100 * sim_list[0][0], 1)) +
                  "% match with " + sim_list[0][1] + "!")

    # build inverted dict
    inv_dict = {}
    for i in range(len(reviews["variety"])):
        inv_dict[reviews["variety"][i]] = i

    i = 0
    dup_list = []
    while len(dup_list) < 3:
        title = sim_list[i][1]
        dup_list.append(title)
        score = round(sim_list[i][0] * 100, 1)
        desc = reviews["personality_description"][inv_dict[title]]
        result.append("[" + str(score) + "%] " + title)
        result.append(desc)
        i += 1
    return result


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
                score = round(sim_list[i][0] * 100, 2)
                desc = reviews["description"][idx]
                wine = "[" + str(score) + "%] " + title + desc
                result.append(wine)
            i += 1
        return result
    except:
        return ["No Results Found"]


def compute_outputs_personality(sim_list, reviews):
    """
    Returns a list of wine variety results based on personality
    """
    result = []
    i = 0
    dup_list = []
    try:
        while len(dup_list) < len(sim_list):
            idx = sim_list[i][1]
            title = reviews["variety"][idx]
            if title not in dup_list:
                # print(title)
                dup_list.append(title)
                score = round(sim_list[i][0] * 100, 2)
                desc = reviews["personality_description"][idx]
                variety = "[" + str(score) + "%] " + title
                result.append(variety)
            i += 1
        return result
    except:
        return ["No Results Found"]