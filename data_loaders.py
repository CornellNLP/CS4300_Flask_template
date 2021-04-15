# from flask import g # global vars; stored per-session, so not very useful
import pickle

def load_works():
    with open('../data/Prototype_Data/workid_to_book_info', 'rb') as f:
        data = pickle.load(f)
    return data
