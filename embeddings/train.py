import sys, os
sys.path.append(os.getcwd())
from gensim.models import Word2Vec
from nltk.tokenize import sent_tokenize, word_tokenize
from data_tools import get_descriptor, get_wine_data, get_beer_data, normalize
from sklearn.feature_extraction.text import TfidfVectorizer
from app.irsystem.models.database import add_drink_batch, Drink
import numpy as np

def main():
    wine_data = get_wine_data(25000)
    wine_desc = [str(x) for x in list(wine_data['description'])]
    beer_data = get_beer_data(25000)
    beer_desc = [str(x) for x in list(beer_data['review/text'])]
    full_text = ' '.join(wine_desc) + ' ' + ' '.join(beer_desc)
    sentences = sent_tokenize(full_text)
    
    norm_sentences = [normalize(s) for s in sentences]

    # TODO(@dana) List of word lists (lol) for each sentence in corpus after
    # removing stop words, normalizing tokens, and phrasing using n-grams
    sentences = []

    # Replace tokens with descriptors when possible
    final_sentences = []
    for s in sentences:
        final_s = []
        for w in s:
            desc_w = get_descriptor(w)
            final_s.append(desc_w)
        final_sentences.append(final_s)

    model = Word2Vec(final_sentences, size=300, min_count=5, iter=15)

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
