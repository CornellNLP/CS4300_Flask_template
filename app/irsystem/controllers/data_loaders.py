from flask import g # stored per-session? so if we get weird data-not-found errors, that's why
import pickle

def load_works():
    if 'works' not in g:
        with open('../data/Prototype_Data/workid_to_book_info', 'rb') as f:
            data = pickle.load(f)
        g.works = data