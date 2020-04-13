from gensim.models import Word2Vec
from data_tools import get_descriptor

def main():
    sentences = [] # placeholder

    norm_sentences = []
    for s in sentences:
        norm_s = []
        for w in s:
            norm_w = get_descriptor(w)
            norm_s.append(norm_w)
        norm_sentences.append(norm_s)
    
    model = Word2Vec(norm_sentences, size=300, min_count=5, iter=15)
            