from gensim.models import Word2Vec
from data_tools import get_descriptor, get_wine_data, get_beer_data, tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from app.irsystem.models.database import add_drink_batch, Drink
import numpy as np

def main():
    wine_data = tokenize(get_wine_data())
    beer_data = tokenize(get_beer_data())

    # TODO(@dana) List of word lists (lol) for each sentence in corpus after
    # removing stop words, normalizing tokens, and phrasing using n-grams
    sentences = []

    # Replace tokens with descriptors when possible
    norm_sentences = []
    for s in sentences:
        norm_s = []
        for w in s:
            norm_w = get_descriptor(w)
            norm_s.append(norm_w)
        norm_sentences.append(norm_s)

    model = Word2Vec(norm_sentences, size=300, min_count=5, iter=15)

    # List of descriptor words for each drink description
    drink_descs = []
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit(drink_descs)
    tfidf_dict = dict(zip(tfidf.get_feature_names(), tfidf.idf_))

    drinks = []
    for d in drink_descs:
        tokens = d.split(' ')
        word_vectors = []
        for t in tokens:
            if t in tfidf_dict.keys():
                weight = tfidf_dict[t]
                vector = model.wv.get_vector(t)
                word_vectors.append(vector * weight)
        try:
            drink_vector = sum(word_vectors) / len(word_vectors)
        except:
            drink_vector = np.array([])
        drink = Drink(name='', description='', vbytes=drink_vector.tobytes())
    add_drink_batch(drinks)

# main()
