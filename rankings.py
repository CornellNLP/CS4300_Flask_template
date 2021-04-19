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

def get_top(restaurant, max_price, cuisine, ambiance, n):
  price_preference = True
  cuisine_preference = True
  ambiance_preference = True
  if max_price == "":
    price_preference = False
  if cuisine == "":
    cuisine_preference = False
  if ambiance == "":
    ambiance_preference = False
  recs = []
  ranked = get_ranked_restaurants(restaurant, cos_sim_matrix)
  for restaurant_info in ranked: # restaurant_info = (name, sim score)
    if len(recs) == n: # if have enough top places, stop finding more
      break
    name = restaurant_info[0] # name of restaurant
    price = int(data["BOSTON"][name]["price"]) # price preference
    # no filtering
    if (not price_preference) and (not cuisine_preference) and (not ambiance_preference):
      print("no filtering")
      recs.append(name)
    else:
      cuisines = data["BOSTON"][name]["categories"] # array of tagged cuisines
      ambiances = data["BOSTON"][name]["ambience"] # array of tagged cuisines
      print(type(ambiances))
      if ambiances is None:
        ambiances = {}
      elif len(ambiances) == 0:
        ambiances = {}
      else:
        ambiances = ast.literal_eval(ambiances)
      #try:
        #ambiances = json.loads(ambiances)
      #except json.decoder.JSONDecodeError:
        #ambiances = {}
      #ambiances = eval(ambiances)
      #print(ambiances)
      #print(type(ambiances))

      price_match = False
      cuisine_match = False
      ambiance_match = False #False

      #if len(ambiances) != ""
      #if len(ambiances) != 0: # if restaurant has ambiance info
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
      if ambiance_preference: # if there is a ambiance preference
            # print(ambiance)
            # print(type(ambiance))
            # print(json.loads(ambiances))
            # print(type(json.loads(ambiances)))
            # print(ambiances)
            # print(type(ambiances))
        print("!!!!!")
        print(ambiance)
        #print(len(ambiances))
        if ambiances:
          print("in if")
          if ambiances[ambiance]:
            ambiance_match = True
      else: # no cuisine preference
        ambiance_match = True

      if ambiance_match and cuisine_match and price_match:
        recs.append(name)
  return recs

# def get_top(restaurant):
#   #get the restaurant name
#   return get_ranked_restaurants(restaurant, cos_sim_matrix)

# def get_restaurant_to_index():
#   return restaurant_to_index
if __name__ == '__main__':
  main()
