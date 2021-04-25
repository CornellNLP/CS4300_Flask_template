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

def get_ranked_restaurants(in_restaurant, sim_matrix):
  # input restaurant will have 11 reviews
  # find every row that corresponds to a review for input restaurant
  # take the average of them
  # group by every 10
  rest_idx = restaurant_to_index[in_restaurant]
  review_ids = review_idx_for_restaurant[in_restaurant]
  review_sims = sim_matrix[review_ids]
  review_sims = np.mean(review_sims, axis=0)
  restaurant_sims = [np.mean(arr) for arr in np.split(review_sims, review_splitter)]
  rest_lst = [(index_to_restaurant[i], s) for i,s in enumerate(restaurant_sims)]
  rest_lst = rest_lst[:rest_idx] + rest_lst[rest_idx+1:]
  rest_lst = sorted(rest_lst, key=lambda x: -x[1])
  return rest_lst


def main():
  #get the restaurant name
  top_restaurants = get_ranked_restaurants("Boloco", cos_sim_matrix)
  print(len(top_restaurants))
  for restaurant in top_restaurants[:3]:
    name = restaurant[0]
    print("RESTAURANT: ", name)
    #for rev in small_data[name]['reviews'][0]:
        #print(rev['text'])
        #print("///////")
    print("")

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

def get_top(restaurant, max_price, cuisine, ambiance, n, review_weight, ambiance_weight):
  price_preference = True
  cuisine_preference = True
  ambiance_preference = True
  if max_price == "":
    price_preference = False
  if cuisine == "":
    cuisine_preference = False

  recs = []
  ranked = get_ranked_restaurants(restaurant, cos_sim_matrix)

  # split up ranked into a list of names and list of similarity scores
  ranked_names = []
  ranked_cossims = []
  # going to be used for jaccard (all restaurants' ambiances)
  restaurant_ambiances = []

  for rest in ranked:
    ranked_names.append(rest[0])
    ranked_cossims.append(rest[1])
    restaurant_ambiances.append(data["BOSTON"][rest]["ambience"])
  
  # not sure what ambiance is (string or list) - turn into a list
  user_and_rest_ambiances = ambiance + data["BOSTON"][restaurant]["ambience"]

  jaccard_list = getJaccard(user_and_rest_ambiances, restaurant_ambiances)

  weighted_rankings = []
  weighted_name_ranks = []

  if user_and_rest_ambiances == "":
    ambiance_preference = False
    weighted_name_ranks = ranked
  else:
    weighted_cossim = [el * review_weight for el in ranked_cossims]
    weighted_jaccard = [el * ambiance_weight for el in jaccard_list]
    weighted_rankings = [x + y for x, y in zip(weighted_cossim, weighted_jaccard)]
    for i in range(len(ranked_names)):
      weighted_name_ranks.append((ranked_names[i], weighted_rankings[i]))
    weighted_name_ranks = sorted(weighted_name_ranks, key=lambda x: -x[1])

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
      # ambiances = data["BOSTON"][name]["ambience"] # array of tagged cuisines
      # if ambiances is None:
      #   ambiances = {}
      # elif len(ambiances) == 0:
      #   ambiances = {}  
      # else:
      #   ambiances = ast.literal_eval(ambiances)

      price_match = False
      cuisine_match = False
      # ambiance_match = False 

      if price_preference: # if there is a price preference
        if ((max_price == "low") and (price <= 1)) or ((max_price == "medium") and (price <= 3)) or ((max_price == "high") and (price <= 5)):
          price_match = True
      else: # no price preference
        price_match = True

      if cuisine_preference: # if there is a cuisine preference
        if cuisine in cuisines:
            cuisine_match = True
      else: # no cuisine preference
        cuisine_match = True

      # if user_and_rest_ambiances: # if there is a ambiance preference
      #   if ambiances:
      #     if ambiances[ambiance]:
      #       ambiance_match = True
      # else: # no ambiance preference
      #   ambiance_match = True

      # if ambiance_match and cuisine_match and price_match:
      if cuisine_match and price_match:
        recs.append(name)
  return recs

# def get_top(restaurant):
#   #get the restaurant name
#   return get_ranked_restaurants(restaurant, cos_sim_matrix)

# def get_restaurant_to_index():
#   return restaurant_to_index

def web_scraping(restaurants):
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
    number = float(rating_text.split(' ')[0])
    info['star rating'] = number
    info['categories'] = small_data[r]['categories']
    full_info[r] = info
    print("restaurant scraped")
  return full_info


      
    


if __name__ == '__main__':
  main()
