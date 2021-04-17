import pandas as pd
import statistics
import re
import numpy as np
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer


def load_data():
    df = pd.read_csv('app/irsystem/models/ski_reviews.csv', header= 1)
    dataframe = pd.DataFrame(df)
    nump_data = dataframe.to_numpy()

    dict_ski = {}
    num_states = 0 
    num_locs = 0
    
    for data in nump_data :
        state = str(data[1])
        ski_area = str(data[2])
        reviewer = str(data[3])
        date = data[4]
        rating = data[5]
        review = str(data[6])
    
        if state in dict_ski:
            if ski_area in dict_ski[state]: 
                dict_ski[state][ski_area].append((date, reviewer, rating, review,state))
            else: 
                dict_ski[state][ski_area] = [(date, reviewer, rating, review,state)] 
                num_locs += 1 
        else: 
            num_states += 1 
            num_locs += 1
            dict_ski[state] = {ski_area: [(date, reviewer, rating, review,state)]}
            
    return dict_ski 


def build_vectorizer(max_n_terms=5000, max_prop_docs=0.8, min_n_docs=10):
    vectorizer = TfidfVectorizer(min_df = min_n_docs, max_df = max_prop_docs, max_features = max_n_terms, stop_words = "english")
    return vectorizer 


def pre_vectorize(query ,dict_ski):
    state_locs =  list(dict_ski.values())
    state_names = list (dict_ski.keys())
    location_names = []
    reviews_by_loc = [('query',query)]

    for loc in state_locs: 
        location_names.extend(list(loc.keys()))
        for site in loc: 
            site_revs = []
            site_str = " "
            site_revs.extend([tup[3] for tup in loc[site]])
            reviews_by_loc.append((site, site_str.join(site_revs),loc))
    return reviews_by_loc 

def ski_site_to_index (reviews_by_loc): 
    return {site:index for index, site in enumerate([site[0] for site in reviews_by_loc])}

def ski_index_to_site (reviews_by_loc): 
    return {index:site for index, site in enumerate([site[0] for site in reviews_by_loc])}

def vectorize (reviews_by_loc, vectorizer = build_vectorizer(max_n_terms=5000, max_prop_docs=0.8, min_n_docs=10)):
    tfidf_vec = vectorizer
    tfidf_mat = tfidf_vec.fit_transform([site[1] for site in reviews_by_loc]).toarray()
    index_to_vocab = {i:v for i, v in enumerate(tfidf_vec.get_feature_names())}
    vocab_to_index = {v:i for i, v in enumerate(tfidf_vec.get_feature_names())}
    return tfidf_mat, index_to_vocab, vocab_to_index


def get_cos_sim(loc1, loc2, input_mat, 
                site_to_index=ski_site_to_index):
    """Returns the cosine similarity of reviews from two locations 
    """
    loc1_tf = input_mat[site_to_index[loc1]]
    loc2_tf = input_mat[site_to_index[loc2]]
    cossim = np.dot(loc1_tf, loc2_tf)/ (np.linalg.norm(loc1_tf) * np.linalg.norm(loc2_tf))
    
    return cossim

def build_sims_cos(tfidf_mat):

    trans_input = np.transpose(tfidf_mat)
    numer = np.dot(tfidf_mat, trans_input)
    denom = np.linalg.norm(tfidf_mat, axis = 1)
    denom_new = denom[:, np.newaxis]
    denom_final = np.multiply (denom, denom_new) 
    fin = np.divide(numer,denom_final)
    
    return fin 

def most_sim (sim_mat,ski_index_to_site, rev_by_loc): 
    most_sim = sim_mat[0]
    sim = []
    count = 0
    for i in most_sim: 
        sim.append((i,ski_index_to_site[count]))
        count += 1
    
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
    reviews_by_loc = pre_vectorize(query ,ski_dict)
    ski_site_to_index1 = ski_site_to_index (reviews_by_loc)
    ski_index_to_site1 = ski_index_to_site (reviews_by_loc)
    tfidf_mat, index_to_vocab, vocab_to_index = vectorize (reviews_by_loc, vectorizer)
    sim_mat = build_sims_cos(tfidf_mat)
    results = most_sim (sim_mat, ski_index_to_site1, ski_dict) 
    return results
    
    
    
    
    
    
    
    
    
