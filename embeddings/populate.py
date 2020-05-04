import sys, os
sys.path.append(os.getcwd())
from .data_tools import *
from nltk.tokenize import sent_tokenize
from app.irsystem.models.database import *
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec
from gensim.models.phrases import Phrases, Phraser
from math import isnan
import numpy as np
import pickle
import re
import json

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

def make_embeddings(wv, tfidf_dict):
    embeddings = []
    for word in get_descriptors():
        if word in tfidf_dict and word in wv.vocab:
            weight = tfidf_dict[word]
            vector = wv.get_vector(word)
            vbytes = json.dumps((vector * weight).tolist())
            embeddings.append(Embedding(
                word=word,
                vbytes=vbytes
            ))
        else:
            print('Descriptor not seen in training: {}'.format(word))
    return embeddings

def make_drinks(df, descriptors, dtype, wv, tfidf_dict, min_desc):
    h = HEADERS[dtype]
    drinks = []
    for i in range(len(df)):
        row = df.iloc[i]
        tokens = descriptors[i].split(' ')
        if len(tokens) < min_desc:
            continue
        word_vectors = []
        for t in tokens:
            if t in tfidf_dict:
                weight = tfidf_dict[t]
                vector = wv.get_vector(t)
                word_vectors.append(vector * weight)
        drink_vector = sum(word_vectors) / len(word_vectors)
        # Required/expected fields
        name = row[h.name]
        desc = row[h.desc]
        vbytes = json.dumps(drink_vector.tolist())
        url = row[h.url]
        drink = Drink(name=name, description=desc, vbytes=vbytes, type=dtype, url=url)
        # Optional fields
        if h.price is not None:
            price = row[h.price]
            if not isnan(price):
                drink.price = price
        if h.origin is not None:
            drink.origin = row[h.origin]
        if h.abv is not None:
            raw_abv = row[h.abv]
            if type(raw_abv) == str:
                raw_abv = raw_abv.split('-')[0]
                raw_abv = re.sub(r"^\D*", '', raw_abv).replace('%', '')
                if raw_abv == '':
                    drink.abv = None
                else:
                    drink.abv = float(raw_abv)
            else:
                drink.abv = raw_abv
        if h.reviews is not None:
            drink.reviews = json.dumps(row[h.reviews])
        if h.rating is not None:
            drink.rating = row[h.rating]
        if h.base is not None:
            drink.base = row[h.base]
        drinks.append(drink)
    return drinks

def main(model_file=None, phraser_file=None, tfidf_file=None, wine_size=None,
         beer_size=None, add_embeddings=True, add_drinks=True, use_reviews=True,
         min_desc=4):
    if model_file is None or phraser_file is None:
        print('Fetching wine training data...')
        wine_train_data = get_wine_train_data(wine_size)
        wine_train_desc = [str(x) for x in list(wine_train_data['description'])]
        print('Fetching beer training data...')
        beer_train_data = get_beer_train_data(beer_size)
        beer_train_desc = [str(x) for x in list(beer_train_data['review/text'])]
        full_text = ' '.join(wine_train_desc + beer_train_desc)
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

    print('Fetching drink data to populate database...')
    wines = get_wines()
    beers = get_beers()
    liquors = get_liquors()
    cocktails = get_cocktails()
    cocktail_desc = list(cocktails['description'])
    if use_reviews:
        wine_desc = [d + ' '.join([rev['body'] for rev in r if rev['body'] is not None]) for d, r in zip(
            wines['description'].fillna(''), wines['reviews']
        )]
        beer_desc = [d + ' '.join([rev['body'] for rev in r if rev['body'] is not None]) for d, r in zip(
            beers['description'].fillna(''), beers['reviews']
        )]
        liquor_desc = [d + ' '.join([rev['body'] for rev in r if rev['body'] is not None]) for d, r in zip(
            liquors['description'].fillna(''), liquors['reviews']
        )]
    else:
        wine_desc = list(wines['description'].fillna(''))
        beer_desc = list(beers['description'].fillna(''))
        liquor_desc = list(liquors['description'].fillna(''))

    # List of descriptor words for each drink description
    print('Extracting descriptors...')
    wine_descriptors = extract_desc(wine_desc, phraser)
    beer_descriptors = extract_desc(beer_desc, phraser)
    liquor_descriptors = extract_desc(liquor_desc, phraser)
    cocktail_descriptors = extract_desc(cocktail_desc, phraser)
    
    if tfidf_file is None:
        print('Calculating TF-IDF...')
        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit(
            wine_descriptors +
            beer_descriptors +
            liquor_descriptors +
            cocktail_descriptors
        )
        tfidf_dict = dict(zip(tfidf.get_feature_names(), tfidf.idf_))
        # with open('embeddings/trained/tfidf_p4.pkl', 'wb') as fp:
        #     pickle.dump(tfidf_dict, fp)
    else:
        with open(tfidf_file, 'rb') as fp:
            tfidf_dict = pickle.load(fp)

    if add_embeddings:
        print('Creating Embedding objects...')
        embeddings = make_embeddings(model.wv, tfidf_dict)
        add_embedding_batch(embeddings)
        print('{} Embeddings added to database!'.format(len(embeddings)))

    if add_drinks:
        drinks = []
        print('Creating Drink objects...')
        drinks += make_drinks(wines, wine_descriptors, 'wine', model.wv, tfidf_dict, min_desc)
        drinks += make_drinks(beers, beer_descriptors, 'beer', model.wv, tfidf_dict, min_desc)
        drinks += make_drinks(liquors, liquor_descriptors, 'liquor', model.wv, tfidf_dict, min_desc)
        drinks += make_drinks(cocktails, cocktail_descriptors, 'cocktail', model.wv, tfidf_dict, min_desc)
        add_drink_batch(drinks)
        print('{} Drinks added to database!'.format(len(drinks)))

main(
    model_file='embeddings/trained/model_50k.bin',
    phraser_file='embeddings/trained/trigram_50k.pkl',
    tfidf_file='embeddings/trained/tfidf_p4.pkl',
    # add_embeddings=False,
    # add_drinks=False,
)
