import json

output_file = open('finalData.json', 'w')
review_file = open('yelp_academic_dataset_review.json', 'r')
business_file = open('yelp_academic_dataset_business.json', 'r')

"""
#final json will be a dic where the keys are a city and state (ex: "New York, NY")
#these keys then map to a new dic, where the keys are the restaurants names.
#the names map to a dic of the rest of the info about the restaurant (star rating,
#list of reviews, etc.)

EXAMPLE:
{"ITHACANY: {"PURITYICECREAM":{reviews:[], attributes:[], ...}, "COLLEGETOWNBAGELS":{...}},
"NEWYORKNY: {...},
"BOSTONMA: {...}}

#initialize new json, this will be one large json where the keys are the 
#business_ids and the values are another dic of everything else
#i think this will make it easier to merge the reviews json and the business one
json_merge = {}
"""
#filter business file
for line in business_file:
  current_json = json.loads(line) #turns each individual json line into a dic
  
  #check if it's a restaurant (look at categories (a list) and see if "restaurant"
  #is in there), if it's in the US, and if it has >= 5 reviews

  #if all are true, make a new dic with name, city, state, zip code,
  #and attributes. add a "reviews" field and initialize as a list
  #add to json_merge this business_id as a key and the new dic as the value

for line in review_file:
  current_json = json.loads(line)

  #check the business_id key of the current_json. if this id is a key in 
  #json_merge, create a new dic with the stars, useful, and text part of the
  #review and add the new dic to the corresponding "review" list in json_merge

json_to_write = {}
for key in json_merge:
  city_dic = {}
  #create a new entry in the json_to_write dic. the key is the loc variable 
  city = json_merge[key]["city"]
  state = json_merge[key]["state"]
  loc = city.upper() + state.upper()business name 
  loc.replace(" ","") #remove spaces
  #for example, new york city will have a loc variable of NEWYORKNY

  #the value will be another dic where the keys are the restaurant names
  #and the values are the info/reviews of the restaurants
  name = json_merge[key]["name"]
  name.replace(" ","")
  name.upper()

#put new json/dataset into output file
json.dump(json_to_write, output_file)
