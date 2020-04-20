import sys, os
sys.path.append(os.getcwd())
from data_tools import get_wine_data, get_beer_data, get_descriptor, normalize, HEADERS
from nltk.tokenize import sent_tokenize
from app.irsystem.models.database import Drink, add_drink_batch, query_drink
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec
from gensim.models.phrases import Phrases, Phraser
from math import isnan
import numpy as np

def train(norm_sentences, phraser):
    print('Phrasing data...')
    # List of string lists for each sentence in corpus after normalizing and
    # phrasing using n-grams
    phr_sentences = [phraser[s] for s in norm_sentences]

    print('Inserting descriptors...')
    # Replace tokens with descriptors when possible
    final_sentences = [[get_descriptor(w, False) for w in s] for s in phr_sentences]

    print('Training model...')
    model = Word2Vec(final_sentences, size=300, min_count=5, iter=15)
    # model.save('embeddings/trained/model.bin')
    return model

def extract_desc(lst, phraser):
    descriptors = []
    for text in lst:
        norm = normalize(text)
        phr = phraser[norm]
        desc = [get_descriptor(w, True) for w in phr]
        final = [str(w) for w in desc if w is not None]
        descriptors.append(' '.join(final))
    return descriptors

def make_drinks(df, descriptors, dtype, wv, tfidf_dict):
    h = HEADERS[dtype]
    drinks = []
    for i in range(len(df)):
        row = df.iloc[i]
        tokens = descriptors[i].split(' ')
        word_vectors = []
        for t in tokens:
            if t in tfidf_dict.keys():
                weight = tfidf_dict[t]
                vector = wv.get_vector(t)
                word_vectors.append(vector * weight)
        try:
            drink_vector = sum(word_vectors) / len(word_vectors)
        except:
            drink_vector = np.array([])
        # Required fields
        name = row[h.name]
        desc = row[h.desc]
        vbytes = drink_vector.tobytes()
        drink = Drink(name=name, description=desc, vbytes=vbytes, type=dtype)
        # Optional fields
        if h.price is not None:
            price = row[h.price]
            if not isnan(price):
                drink.price = price
        if h.origin is not None:
            drink.origin = row[h.origin]
        drinks.append(drink)
    return drinks

def main(model_file=None, phraser_file=None, wine_size=None, beer_size=None):
    print('Fetching wine data...')
    wine_data = get_wine_data(wine_size)
    wine_desc = [str(x) for x in list(wine_data['description'])]
    print('Fetching beer data...')
    beer_data = get_beer_data(beer_size)
    beer_desc = [str(x) for x in list(beer_data['review/text'])]
    full_text = ' '.join(wine_desc + beer_desc)

    if model_file is None or phraser_file is None:
        print('Preprocessing data...')
        # List of strings for each sentence in corpus
        sentences = sent_tokenize(full_text)
        norm_sentences = [normalize(s) for s in sentences]

    if phraser_file is None:
        print('Training phraser...')
        bigram = Phrases(norm_sentences)
        trigram = Phrases(bigram[norm_sentences])
        phraser = Phraser(trigram)
        # phraser.save('embeddings/trained/trigram.pkl')
    else:
        phraser = Phraser.load(phraser_file)

    if model_file is None:
        model = train(norm_sentences, phraser)
    else:
        model = Word2Vec.load(model_file)

    # List of descriptor words for each drink description
    print('Extracting descriptors...')
    wine_descriptors = extract_desc(wine_desc, phraser)
    beer_descriptors = extract_desc(beer_desc, phraser)
    
    print('Calculating TF-IDF...')
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit(wine_descriptors + beer_descriptors)
    tfidf_dict = dict(zip(tfidf.get_feature_names(), tfidf.idf_))

    drinks = []
    print('Creating Drink objects...')
    drinks += make_drinks(wine_data, wine_descriptors, 'wine', model.wv, tfidf_dict)
    drinks += make_drinks(beer_data, beer_descriptors, 'beer', model.wv, tfidf_dict)
    add_drink_batch(drinks)
    print('{} Drinks added to database!'.format(len(drinks)))

# main(
#     model_file='embeddings/trained/model_50k.bin',
#     phraser_file='embeddings/trained/trigram_50k.pkl',
#     wine_size=5000,
#     beer_size=5000
# )
