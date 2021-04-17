import json
review_file = open('yelp_academic_dataset_review.json', 'r')
id_review = {}
for line in review_file:
  if line["business_id"] not in id_review.keys():
    id_review["business_id"] = [(line["useful"],line["text"])]
  else:
    id_review["business_id"].append((line["useful"],line["text"]))

  