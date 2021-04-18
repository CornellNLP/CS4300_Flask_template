# from flask import g # global vars; stored per-session, so not very useful
import pickle

def load_data():
    return {
        'works': load_works(),
        'inverted_index': load_inverted(),
        'tfidf': load_tfidf()
    }

def load_works():
    with open('./data/workid_to_book_info', 'rb') as f:
        data = pickle.load(f)
    return data

def load_inverted():
    with open('./data/inverted_index_min=0.8_max=0.99', 'rb') as f:
        data = pickle.load(f)
    return data

def load_tfidf():
    with open('./data/work_tf_idf_vectors_min=0.8_max=0.99_NORMS', 'rb') as f:
        data = pickle.load(f)
    return data
