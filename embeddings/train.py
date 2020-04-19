import sys, os
sys.path.append(os.getcwd())
from gensim.models import Word2Vec
from gensim.models.phrases import Phrases, Phraser
from nltk.tokenize import sent_tokenize, word_tokenize
from data_tools import get_descriptor, get_wine_data, get_beer_data, normalize
from sklearn.feature_extraction.text import TfidfVectorizer
from app.irsystem.models.database import add_drink_batch, Drink
import numpy as np

def main():
    print('Fetching wine data...')
    wine_data = get_wine_data(50000)
    wine_desc = [str(x) for x in list(wine_data['description'])]
    print('Fetching beer data...')
    beer_data = get_beer_data()
    beer_desc = [str(x) for x in list(beer_data['review/text'])]
    full_text = ' '.join(wine_desc) + ' ' + ' '.join(beer_desc)

    print('Preprocessing data...')
    # List of strings for each sentence in corpus
    sentences = sent_tokenize(full_text)
    norm_sentences = [normalize(s) for s in sentences]
    bigram = Phrases(norm_sentences)
    trigram = Phrases(bigram[norm_sentences])
    ngram = Phraser(trigram)
    # List of string lists for each sentence in corpus after normalizing and
    # phrasing using n-grams
    phr_sentences = [ngram[s] for s in norm_sentences]

    # Replace tokens with descriptors when possible
    final_sentences = [[get_descriptor(w) for w in s] for s in phr_sentences]

    print('Training model...')
    model = Word2Vec(final_sentences, size=300, min_count=5, iter=15)
    print(model.wv.similar_by_word('apple'))
    model.save('trained_models/model_all.bin')
    # return

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
