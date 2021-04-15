import json

count = 0
with open('reviews.json', 'w') as output_f:
  with open('yelp_academic_dataset_review.json', 'r') as input_f:
    for line in input_f:
      if count >= 1000:
        break
      else:
        output_f.write(line)
        count += 1
input_f.close()
output_f.close()