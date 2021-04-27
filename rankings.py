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
import ast
from bs4 import BeautifulSoup
import requests
import lxml
import cchardet
import pickle

#code from class demo
word_splitter = re.compile(r"""
    (\w+)
    """, re.VERBOSE)

def getwords(sent):
  return [w.lower() for w in word_splitter.findall(sent)]

#load the vectorizer
with open('vectorizer.pickle', 'rb') as v:
  tfidf_vec = pickle.load(v)


with open("finalData2.json", "r") as f:
  data = json.load(f)

with open("reviewidx2.json", "r") as fp:
  review_idx_for_restaurant = json.load(fp)

#with open("cossim3.npy", "r") as fp2:
  #cos_sim_matrix = np.load(fp2)
cos_sim_matrix = np.array(np.load('cossim4.npy'))
small_data = data['BOSTON']

index_to_restaurant = {i: v for i, v in enumerate(small_data.keys())}

restaurant_to_index = {v: i for i, v in index_to_restaurant.items()}

#sims cos load

review_splitter = [ids[0] for ids in review_idx_for_restaurant.values()][1:]

def get_ranked_restaurants(in_restaurant, sim_matrix, user_review):
  # input restaurant will have 11 reviews
  # find every row that corresponds to a review for input restaurant
  # take the average of them
  # group by every 10

  if not user_review:
    rest_idx = restaurant_to_index[in_restaurant]
    review_ids = review_idx_for_restaurant[in_restaurant]
    review_sims = sim_matrix[review_ids]
    review_sims = np.mean(review_sims, axis=0)
  else:
    review_sims = sim_matrix
  restaurant_sims = [np.mean(arr) for arr in np.split(review_sims, review_splitter)]
  rest_lst = [(index_to_restaurant[i], s) for i,s in enumerate(restaurant_sims)]
  #rest_lst = rest_lst[:rest_idx] + rest_lst[rest_idx+1:]
  rest_lst = sorted(rest_lst, key=lambda x: -x[1])
  return rest_lst
  #rest_idx = restaurant_to_index[in_restaurant]
  #review_ids = review_idx_for_restaurant[in_restaurant]
  #review_sims = sim_matrix[review_ids]
  #review_sims = np.mean(review_sims, axis=0)
  #restaurant_sims = [np.mean(arr) for arr in np.split(review_sims, review_splitter)]
  #rest_lst = [(index_to_restaurant[i], s) for i,s in enumerate(restaurant_sims)]
  #rest_lst = rest_lst[:rest_idx] + rest_lst[rest_idx+1:]
  #rest_lst = sorted(rest_lst, key=lambda x: -x[1])
  #return rest_lst


# def main():
#   #get the restaurant name
#   top_restaurants = get_top("Boloco", "high", "Chinese", [], 5, .5, .5)
#   print(len(top_restaurants))
#   for restaurant in top_restaurants[:3]:
#     name = restaurant
#     print("RESTAURANT: ", name)
#     #for rev in small_data[name]['reviews'][0]:
#         #print(rev['text'])
#         #print("///////")
#     print("")

def getJaccard(input_ambiances, all_rests_ambiances):
  """Returns a list of the size number of restuarants that indicates the jaccard
  sim between the inputted restuarants ambiances and the existing restaurants'
  Returns a list of size number of restuarants total, where entry
  i is the jaccard sim between the inputted restuarants ambiances and the
  restaurants' ambiances from the dataset
  Params: {
    input_ambiances: list
    all_rests_ambiances: list of lists
  }
  Returns: list
  """
  jaccard_ambiances = []
  input_amb = set(input_ambiances)
  for rest_ambiance in all_rests_ambiances:
    intersection = len(input_amb.intersection(rest_ambiance))
    union = len(set(input_ambiances + rest_ambiance))
    jaccard_ambiances.append(intersection/union)
  return jaccard_ambiances

def get_top(restaurant, max_price, cuisine, ambiance, n, review_weight, ambiance_weight, user_review, user_matrix):
  """Returns a list of the top n restuarants that match the inputted restaurant
  and preferences indicated
  Params: {
    restaurant: string
    max_price: string
    cuisine: string
    ambiance: string list
    n: int
    review_weight: float
    ambiance_weight: float
    user_revew: bool
    cosine_matrix: np.ndarray
  }
  Returns: list
  """
  price_preference = True
  cuisine_preference = True
  ambiance_preference = True
  if max_price == "":
    price_preference = False
  if cuisine == "":
    cuisine_preference = False

  recs = []
  print(type(ambiance))
  print(ambiance)
  if not user_review:
    ranked = get_ranked_restaurants(restaurant, cos_sim_matrix, False)
  #rankings for user review
  else:
    ranked = get_ranked_restaurants("", user_matrix, True)

  # split up ranked into a list of names and list of similarity scores
  ranked_names = []
  ranked_cossims = []
  # going to be used for jaccard (all restaurants' ambiances)
  restaurant_ambiances = []

  for rest in ranked:
    ranked_names.append(rest[0])
    ranked_cossims.append(rest[1])
    restaurant_ambiances.append(data["BOSTON"][rest[0]]["ambience"])

  if not user_review:
    user_and_rest_ambiances = list(set(ambiance + (data["BOSTON"][restaurant]["ambience"])))
  else:
    user_and_rest_ambiances = list(ambiance)

  jaccard_list = []
  if len(user_and_rest_ambiances) != 0:
    jaccard_list = getJaccard(user_and_rest_ambiances, restaurant_ambiances)

  weighted_rankings = []
  weighted_name_ranks = []

  if len(user_and_rest_ambiances) == 0:
    ambiance_preference = False
    weighted_name_ranks = ranked
  else:
    weighted_cossim = [el * review_weight for el in ranked_cossims]
    weighted_jaccard = [el * ambiance_weight for el in jaccard_list]
    weighted_rankings = [x + y for x, y in zip(weighted_cossim, weighted_jaccard)]
    for i in range(len(ranked_names)):
      weighted_name_ranks.append((ranked_names[i], weighted_rankings[i]))
    weighted_name_ranks = sorted(weighted_name_ranks, key=lambda x: -x[1])
  # print(weighted_name_ranks[0:10])

  for restaurant_info in weighted_name_ranks: # restaurant_info = (name, weighted sim score)
    if len(recs) == n: # if have enough top places, stop finding more
      break
    name = restaurant_info[0] # name of restaurant
    price = int(data["BOSTON"][name]["price"]) # price preference

    # no filtering
    if (not price_preference) and (not cuisine_preference) and (not ambiance_preference):
      recs.append(name)
    else:
      cuisines = data["BOSTON"][name]["categories"] # array of tagged cuisines

      price_match = False
      cuisine_match = False
      # ambiance_match = False

      if price_preference: # if there is a price preference
        low = (max_price == "low") and (price == 1 or price ==2)
        medium = (max_price == "medium") and (price == 3)
        high = (max_price == "high") and (price == 4 or price == 5)
        if low or medium or high:
          price_match = True
      else: # no price preference
        price_match = True

      if cuisine_preference: # if there is a cuisine preference
        if cuisine in cuisines:
            cuisine_match = True
      else: # no cuisine preference
        cuisine_match = True

      if cuisine_match and price_match and restaurant not in name:
        recs.append(name)

  print(type(recs))
  return recs

# def get_top(restaurant):
#   #get the restaurant name
#   return get_ranked_restaurants(restaurant, cos_sim_matrix)

# def get_restaurant_to_index():
#   return restaurant_to_index

def get_reviews(restaurant):
  reviews = []
  for review in data["BOSTON"][restaurant]["reviews"]:
    reviews.append(review["text"])
  return reviews

def web_scraping(restaurants, input_index, user_review, user_matrix):
  full_info = dict()
  requests_session = requests.Session()
  for r in restaurants:
    info = dict()
    bus_id = small_data[r]['id']
    page = requests_session.get(f"https://www.yelp.com/biz/{bus_id}")
    print("request made")
    soup = BeautifulSoup(page.content, 'lxml')
    photos = soup.findAll('img', {"class": "photo-header-media-image__373c0__2Qf5H"})
    image_srcs = []
    for i, p in enumerate(photos):
      src = p.attrs['src']
      image_srcs.append(src)
    info['photos'] = image_srcs
    # search the title of the webpage for address
    possible_addresses = soup.findAll('title', {"data-rh": "true"})
    if len(possible_addresses) == 0:
      info['address'] = "No address found"
    else:
      address = "No address found"
      for p in possible_addresses:
        if p.get_text() != "":
          address = p.get_text()
          for piece in address.split('- '):
            if "Boston" in piece:
              address = piece
      info['address'] = address
    rating_text = soup.findAll('div', {"class": re.compile("i-stars--large")})[0].attrs['aria-label']
    number = round(float(rating_text.split(' ')[0]))
    info['star rating'] = number
    # get rid of word 'Restaurants' in categories list
    categories_string = small_data[r]['categories']
    categories_list = categories_string.split(', ')
    categories_list = [word for word in categories_list if word not in ['Restaurants']]
    info['categories'] = ', '.join(map(str, categories_list))

    full_info[r] = info
    info['reviews'] = get_reviews(r)
    info['id'] = bus_id
    # get sim score of resturaunt by averaging sim scores of reviews
    info['sim_score'] = 0
    if not user_review:
      orig_reviews = review_idx_for_restaurant[r] # list of review ids
      new_reviews = review_idx_for_restaurant[index_to_restaurant[input_index]]
      for i in orig_reviews:
        for j in new_reviews:
          info['sim_score'] += cos_sim_matrix[i][j]
      info['sim_score'] = info['sim_score'] / 4
      # cos_sim_matrix[input_index][restaurant_to_index[r]]
    else:
      orig_reviews = review_idx_for_restaurant[r]
      for i in orig_reviews:
        info['sim_score'] += user_matrix[i]
      info['sim_score'] = info['sim_score'] / 4
    print("restaurant scraped")
  return full_info

if __name__ == '__main__':
  main()
