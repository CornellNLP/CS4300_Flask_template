from collections import defaultdict
from collections import Counter
import json
import math
import string
import time
import numpy as np
from nltk.tokenize import TreebankWordTokenizer
#from IPython.core.display import HTML
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import PorterStemmer
import re
from pathlib import Path

with open("finalData.json", "r") as f:
    data = json.load(f)

#code from a5
def build_vectorizer():
    """Returns a TfidfVectorizer object with certain preprocessing properties.
    
    Params: {max_n_terms: Integer,
             max_prop_docs: Float,
             min_n_docs: Integer}
    Returns: TfidfVectorizer
    """
    return TfidfVectorizer(stop_words = 'english', min_df = 2)

#code from class demo
word_splitter = re.compile(r"""
    (\w+)
    """, re.VERBOSE)

def getwords(sent):
  return [w.lower() 
    for w in word_splitter.findall(sent)]

tfidf_vec = build_vectorizer()
stemmer=PorterStemmer()
if Path("reviewslist.json").exists():
  with open("reviewslist.json") as fp:
    reviews = json.load(fp)
else:
  reviews = []
  for city, city_dic in data.items():
      for restaurant, restaurant_dic in city_dic.items():
          for review in restaurant_dic['reviews']:
              all_words = getwords(review['text'])
              stem_text = [stemmer.stem(t.lower()) for t in all_words]
              reviews.append(" ".join(stem_text))
  with open("reviewslist.json", 'w') as fp:
    json.dump(reviews, fp, indent=2)

print("after building reviews")

tfidf_mat = tfidf_vec.fit_transform(reviews).toarray()

print(tfidf_mat.shape)

print("after build tf idf matrix")

#code from a5
def build_movie_sims_cos(num_reviews, cos_sim, input_doc_mat):
  """Returns a matrix of size num_movies x num_movies where for (i,j), entry [i,j]
      should be the cosine similarity between the movie with index i and the movie with index j
      
  Note: All movies are trivially perfectly similar to themselves, so the diagonals of the output matrix should be 1.
  
  Params: {num_movies: Integer,
            input_doc_mat: Numpy Array,
            movie_index_to_name: Dict,
            movie_name_to_index: Dict,
            input_get_sim_method: Function}
  Returns: Numpy Array 
  """
  #cos_sim = np.zeros((num_movies, num_movies))
  for i in range(num_reviews):
      norm_i = np.linalg.norm(input_doc_mat[i])
      for j in range(num_reviews):
        cos_sim[i][j] = np.dot(input_doc_mat[i], input_doc_mat[j])/(norm_i* np.linalg.norm(input_doc_mat[j]))
  return cos_sim

#sims_cos = build_movie_sims_cos(len(reviews), tfidf_mat)

print("before build initial")

#norms = np.linalg.norm(tfidf_mat, axis=1)
cos_sim = np.zeros((len(reviews), len(reviews)), dtype=np.float16)

cos_sim = build_movie_sims_cos(len(reviews), cos_sim, tfidf_mat)

np.savetxt('cossim.csv', cos_sim, delimiter = ',')

