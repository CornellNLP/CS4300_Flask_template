import json

input_file = open('finalData.json', 'r')
output_file = open('finalDataWithIDs.json', 'w')

review_index = 0 # id for reviews
updated_info = {} # all updated info

for line in input_file:
  city_info = json.loads(line)
  # city = city, city_info = {} containing info such as reviews
  for city in city_info:
    # updated_city_info = {}
    city_traits = city_info[city]
    for restaurant, restaurant_info in city_traits.items():
      review_ids = [] # ids of all reviews for restaurant
      for review in restaurant_info["reviews"]:
        review["id"] = review_index # add id attribute to review
        review_ids.append(review_index) # add id to list of review ids for that restaurant
        review_index += 1

      # update restaurant to have list of ids
      restaurant_info["review_ids"] = review_ids
  updated_info[city] = city_info

#put new json/dataset into output file
output_file.write(json.dumps(updated_info)+'\n')
