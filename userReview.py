import rankings
from nltk.stem import PorterStemmer
import pickle
import json
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

data = rankings.data
def getwords(sent):
  return [w.lower() for w in word_splitter.findall(sent)]
stemmer = PorterStemmer()
def build_vectorizer():
  """Returns a TfidfVectorizer object with certain preprocessing properties.
  
  Params: {max_n_terms: Integer,
            max_prop_docs: Float,
            min_n_docs: Integer}
  Returns: TfidfVectorizer
  """
  return TfidfVectorizer(stop_words = 'english', min_df = 2)

word_splitter = re.compile(r"""
    (\w+)
    """, re.VERBOSE)

small_data = data['BOSTON']

index_to_restaurant = {i: v for i, v in enumerate(small_data.keys())}

restaurant_to_index = {v: i for i, v in index_to_restaurant.items()}


#index_to_vocab = {i:v for i, v in enumerate(tfidf_vec.get_feature_names())} #from class
#vocab_to_index = {v: i for i, v in index_to_vocab.items()}

def filterRestaurants(price_query, cuisine_query):
  """Returns a new list containing the indices of only restaurants that match the
  user's cuisine and price preferences

  Params: {price_query: string,
            cuisine_query: string
            data: dictionary
            }
  Returns: list
  """
  restaurants = data["BOSTON"]
  new_restaurant_indices = []
  for res in restaurants:
    new_restaurant_indices.append(restaurant_to_index[res])
  return new_restaurant_indices
  """
  new_restaurant_indices = [] #list keeping track of all the indices of filtered restaurants
  restaurants = data["BOSTON"]
  for name in restaurants:
    price = int(restaurants[name]["price"])
    cuisine = restaurants[name]["categories"]
    if(price_query != "":
    if ((price_query == "low") and (price <= 2)) or ((price_query == "medium") and (price <= 3 and price > 1)) or ((price_query == "high") and (price <= 5 and price > 3)):
      new_restaurant_indices.append(restaurant_to_index[name]) #add index to list of filtered restaurants
  return new_restaurant_indices
  """
def get_cos_sim(old_review_index, new_review_vector, new_review_norm, input_doc_mat):
  """Returns the cosine similarity of two restaurants.
  
  Params: {old_review_index: int,
            new_review_vector: np.ndarray,
            new_review_norm: int,
            input_doc_mat: np.ndarray,
            }
  Returns: Float 
  """
  #get indicies of movie1 and movie2 and get their tf-idf vectors
  #mov1_index = movie_name_to_index[mov1]
  #mov2_index = movie_name_to_index[mov2]
  #mov1_vector = input_doc_mat[mov1_index]
  old_review_vector = input_doc_mat[old_review_index]
  #get dot product of the vectors
  dot = np.dot(new_review_vector, old_review_vector)
  #get norms of both vectors
  old_review_norm = np.linalg.norm(old_review_vector)
  denom = new_review_norm * old_review_norm
  return dot/denom


def computeCosine(review, filter_restaurants):
  """Returns a matrix of size 1 x number of reviews total, where entry
  matrix[i] is the cosine similarity between the new review and review [i]
  Params: {
    review: string
    filter_restaurants: list
    tfidf_mat: np.ndarray
    data: dictionary
  }
  Returns: np.ndarray
  """
  #load the vectorizer (unfitted)
  #with open('vectorizer.pickle', 'rb') as v:
    #tfidf_vec = pickle.load(v)
  tfidf_vec = build_vectorizer()
  
  with open('reviewslist2.json', 'r') as f:
    reviews_list = json.load(f)

  all_words = getwords(review)
  stem_text = [stemmer.stem(t.lower()) for t in all_words if bool(re.match(r"^[a-zA-Z]+$", t))]
 
  #create tf idf matrix
  tfidf_mat = tfidf_vec.fit_transform(reviews_list).toarray()
  print(tfidf_mat.shape)
  print(np.sum(tfidf_mat))
  #convert review to a vector
  reviews = []
  reviews.append(" ".join(stem_text))
  review_vector = tfidf_vec.transform(reviews).toarray()
  print(review_vector.shape)
  print(np.sum(review_vector))
  review_norm = np.linalg.norm(review_vector)
  
  #calculate the cos similarities between new review and other restaurants
  cos_similarities = np.zeros(len(reviews_list))
  print(len(reviews_list))
  for res_index in filter_restaurants:
    res_name = rankings.index_to_restaurant[res_index]
    #get the reviews corresponding to that restaurant
    review_ids = rankings.review_idx_for_restaurant[res_name]
    #print("hello")
    #print(review_ids)
    for rev in review_ids:
      cos_sim = get_cos_sim(rev, review_vector, review_norm, tfidf_mat)
      cos_similarities[rev] = cos_sim
  #print(np.sum(cos_similarities))
  #print(cos_similarities.shape)
  #print(cos_similarities)
  return cos_similarities


#def getCosineRestaurants(review, filter_restaurants):
  """Returns a np array where np[i] is the cosine similarity between the new
  review and restaurant i
  Params: {
    review: string
    filter_restaurants: list (of only the relevant restaurants/ones that fit the query)
  }
  """
  """
  #compute the cosine similarities between new review and the relevant old reviews
  review_cosines = computeCosine(review, filter_restaurants, tfidf_mat)

  #initialize a numpy array of size = number of restaurants
  restaurant_cosines = np.zeros(len(data["BOSTON"]))
  for res in filter_restaurants:
    res_name = rankings.index_to_restaurant[res]
    review_ids = rankings.review_idx_for_restaurant[res_name]
    val1 = review_cosines[review_ids[0]]
    val2 = review_cosines[review_ids[1]]
    avg = (val1 + val2)/2
    #update the cosine sim for the restaurant
    restaurant_cosines[res] = avg

  return restaurant_cosines
"""