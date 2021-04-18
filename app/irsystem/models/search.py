import pandas as pd
import matplotlib.pyplot as plt
import statistics
import re
import numpy as np
import nltk
import csv
import json
from collections import defaultdict, Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import time
import math


def write_csv_to_json(csv_path="ski_reviews.csv", json_path="ski_reviews.json"):
    with open(csv_path, "r") as f:
        with open(json_path, "w") as j:
            reader = csv.reader(f)
            data = {}
            reviews = []
            isFirstLine = True
            for line in reader:
                if isFirstLine:
                    isFirstLine = False
                    continue
                row_num, state, area, reviewer, date, rating, text = line[
                    0], line[1], line[2], line[3], line[4], line[5], line[6]
                review = {
                    "state": state,
                    "area_name": area,
                    "reviewer_name": reviewer,
                    "review_date": date,
                    "rating": rating,
                    "text": text
                }
                data[row_num] = review
            json.dump(data, j)
    return


def load_json(file):
    with open(file, "r") as f:
        data = json.load(f)
        return data


def write_json(data, file):
    with open(file, "w") as f:
        json.dump(data, f)
    return


def load_data_from_json(file="ski_reviews.json"):
    return load_json(file)


def load_data(debug=False):
    if not debug:
        df = pd.read_csv('app/irsystem/models/ski_reviews.csv', header=1)
    else:
        df = pd.read_csv('ski_reviews.csv', header=1)
    dataframe = pd.DataFrame(df)
    nump_data = dataframe.to_numpy()

    dict_ski = {}
    num_states = 0
    num_locs = 0

    for data in nump_data:
    num_states = 0
    num_locs = 0

    for data in nump_data:
        state = str(data[1])
        ski_area = str(data[2])
        reviewer = str(data[3])
        date = data[4]
        rating = data[5]
        review = str(data[6])

        if state in dict_ski:
            if ski_area in dict_ski[state]:
                dict_ski[state][ski_area].append(
                    (date, reviewer, rating, review, state))
            else:
                dict_ski[state][ski_area] = [
                    (date, reviewer, rating, review, state)]
                num_locs += 1
        else:
            num_states += 1
            num_locs += 1
            dict_ski[state] = {ski_area: [
                (date, reviewer, rating, review, state)]}

    return dict_ski


def build_vectorizer(max_n_terms=5000, max_prop_docs=0.8, min_n_docs=10):
    vectorizer = TfidfVectorizer(
        min_df=min_n_docs, max_df=max_prop_docs, max_features=max_n_terms, stop_words="english")
    return vectorizer


def pre_vectorize(query, dict_ski):
    # list of dicts where dict[ski_area] = [review1, review2, ...]
    state_locs = list(dict_ski.values())

    # list of state names
    state_names = list(dict_ski.keys())
    b = True
    location_names = []  # this accumulates the names of all ski areas
    reviews_by_loc = [('query', query)]
    for loc in state_locs:
        # loc is dictionary with keys=area names, values= list of reviews for each area
        # loc.keys() gives all the ski areas in this state
        # location_names.extend(list(loc.keys()))
        location_names += list(loc.keys())
        for site in loc:
            # site is the area name, loc[site] is the list of reviews
            site_revs = []
            site_str = " "
            # site_revs.extend([tup[3] for tup in loc[site]])
            # for each review, extract the text part of the review and add it to site_revs
            # site_revs is a list of all the text reviews for this area name
            site_revs += [tup[3] for tup in loc[site]]
            # site_str.join... is the concatenated string of all reviews' text
            # so we append a tuple (areaname, string of all reviews, dictionary)
            reviews_by_loc.append((site, site_str.join(site_revs), loc))

    # returns a list of tuples, one tuple for each ski area
    return reviews_by_loc


def ski_site_to_index(reviews_by_loc):
    return {site: index for index, site in enumerate([site[0] for site in reviews_by_loc])}


def ski_index_to_site(reviews_by_loc):
    return {index: site for index, site in enumerate([site[0] for site in reviews_by_loc])}


def vectorize(reviews_by_loc, vectorizer=build_vectorizer(max_n_terms=5000, max_prop_docs=0.8, min_n_docs=10)):
    tfidf_vec = vectorizer
    # param is a list: [string of all reviews concatenated for each ski area]
    tfidf_mat = tfidf_vec.fit_transform(
        [site[1] for site in reviews_by_loc]).toarray()
    index_to_vocab = {i: v for i, v in enumerate(
        tfidf_vec.get_feature_names())}
    vocab_to_index = {v: i for i, v in enumerate(
        tfidf_vec.get_feature_names())}
    return tfidf_mat, index_to_vocab, vocab_to_index


def get_tfidf_mat_and_idx(data, query, vectorizer=build_vectorizer()):
    reviews = [review['text'] for row_num, review in data.items()]
    index_to_area_name = {i: data[key]["area_name"]
                          for i, key in enumerate(data)}
    corpus = [query] + reviews
    mat = vectorizer.fit_transform(corpus).toarray()
    # mat = vectorizer.fit_transform(corpus)
    index_to_vocab = {i: v for i, v in enumerate(
        vectorizer.get_feature_names())}
    vocab_to_index = {v: i for i, v in enumerate(
        vectorizer.get_feature_names())}
    return mat, index_to_vocab, vocab_to_index, index_to_area_name


def get_cos_sim(loc1, loc2, input_mat,
                site_to_index=ski_site_to_index):
    """Returns the cosine similarity of reviews from two locations
    """
    loc1_tf = input_mat[site_to_index[loc1]]
    loc2_tf = input_mat[site_to_index[loc2]]
    cossim = np.dot(loc1_tf, loc2_tf) / \
        (np.linalg.norm(loc1_tf) * np.linalg.norm(loc2_tf))

    return cossim


def build_sims_cos(tfidf_mat):

    trans_input = np.transpose(tfidf_mat)
    numer = np.dot(tfidf_mat, trans_input)
    denom = np.linalg.norm(tfidf_mat, axis=1)
    denom_new = denom[:, np.newaxis]
    denom_final = np.multiply(denom, denom_new)
    fin = np.divide(numer, denom_final)

    return fin


def build_cos_sim_vect(tfidf):
    query_row = tfidf[0]
    # print("q", query_row.shape)
    trans = np.transpose(tfidf)
    # print("mat", trans.shape)
    num = np.matmul(query_row, trans)
    # print("mul", num.shape)
    norm = np.sqrt(np.sum(np.square(tfidf), axis=1))
    # print("norm", norm.shape)
    # print(np.sum(norm == 0))
    return (num/norm)[1:]


def most_sim(sim_mat, ski_index_to_site, rev_by_loc):
    # the first row is the similarity between the query and each concatenated string by area
    most_sim = sim_mat[0]
    sim = []
    count = 0
    for i in most_sim:
        sim.append((i, ski_index_to_site[count]))
        count += 1
    # sim is a list of tuples: (similarity score, area name)
    x = sorted(sim, key=lambda x: x[0], reverse=True)
    top_3_rankings = x[1:4]
    top_3_locs = [a[1] for a in top_3_rankings]

    out = '''

The three ski resorts we think you will like best are...

    1. {} located in
    2. {} located in
    3. {} located in
'''

    return (top_3_locs)


def search_q(query, ski_dict):
    vectorizer = build_vectorizer()
    reviews_by_loc = pre_vectorize(query, ski_dict)
    ski_site_to_index1 = ski_site_to_index(reviews_by_loc)
    ski_index_to_site1 = ski_index_to_site(reviews_by_loc)
    tfidf_mat, index_to_vocab, vocab_to_index = vectorize(
        reviews_by_loc, vectorizer)
    sim_mat = build_sims_cos(tfidf_mat)
    results = most_sim(sim_mat, ski_index_to_site1, ski_dict)
    return results


def replace_nans_with_zero(result):
    return [(0, area) if math.isnan(score) else (score, area) for score, area in result]


def average_sim_vect_by_area(result, index_to_area_name):
    area_to_total, area_to_count = defaultdict(float), defaultdict(int)
    for score, area in result:
        area_to_total[area] += score
        area_to_count[area] += 1
    return [(area, area_to_total[area]/area_to_count[area]) for area in area_to_total]


def get_results_from_sim_vector(sim_vect, index_to_area_name):
    result = [(sim, index_to_area_name[i]) for i, sim in enumerate(sim_vect)]
    # print(np.sum([tup[0] == 0 for tup in result]))
    # return sorted(result, key=lambda x: x[0], reverse=True)
    replace = replace_nans_with_zero(result)
    # print(np.sum([tup[0] == 0 for tup in replace]))
    avg = average_sim_vect_by_area(replace, index_to_area_name)
    return sorted(avg, key=lambda x: x[1], reverse=True)


def most_sim(sim_mat, ski_index_to_site):
    most_sim = sim_mat[0]
    sim = []
    count = 0
    for i in most_sim:
        sim.append((i, ski_index_to_site[count]))
        count += 1

    x = sorted(sim, key=lambda x: x[0], reverse=True)
    top_4_rankings = x[1:5]

    return top_4_rankings


def search(query, ski_dict):
    vectorizer = build_vectorizer()
    reviews_by_loc = pre_vectorize(query, dict_ski)
    ski_site_to_index = ski_site_to_index(reviews_by_loc)
    ski_index_to_site = ski_index_to_site(reviews_by_loc)
    tfidf_mat, index_to_vocab, vocab_to_index = vectorize(
        reviews_by_loc, vectorizer)
    sim_mat = build_sims_cos(tfidf_mat)
    results = most_sim(sim_mat, ski_index_to_site)
    return results
