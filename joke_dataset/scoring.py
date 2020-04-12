################ DATA PRE-PROCESSING #################
# Run file to ... 
# 1. Standardizes + Normalizes Scores
# 2. Delete Duplicate Jokes (avg. scores of duplicates, combine categories of duplicates)

from sklearn.preprocessing import StandardScaler, MinMaxScaler
import numpy as np
from glob import glob
import json
from pathlib import Path
import os

#################### 1. STANDARDIZE AND NORMALIZE SCORES #########################

# Standardize scores across individual data sources
Path('/root/dir/sub/file.ext').stem
scaler = StandardScaler()
minmax_scaler = MinMaxScaler(feature_range = (2.5, 5))

final = []
for filename in glob('./json/data_nopreprocess/*.json'):
    name = Path(filename).stem

    with open(filename) as f:
        data = json.load(f) 
        scores_train = [obj['score'] for obj in data]
        if (scores_train[0] is not None): 
            scores_train = np.array_split(scores_train, len(scores_train))
           
            # standardize scoring, then normalize to [2.5, 5]
            scores_scaled = scaler.fit_transform(scores_train)
            for i in range(0, len(data)):
                data[i]['score'] = scores_scaled[i][0]
        final += data
        f.close()
    
    path = os.path.join('./json/data_preprocess', name + "." + "json")
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
        f.close()

# Combine all files in  './raw/data_nopreprocess' into '.final/json' w/ standardized Scores
with open('./final.json', 'w') as f:
    json.dump(final, f, indent=4)
    f.close()

# Normalize scores in './final.json'
with open ('./final.json') as f:
    data = json.load(f)
    scores_train = [obj['score'] for obj in data]
    scores_train = np.array_split(scores_train, len(scores_train))
    # normalize scoring from [min, max] to [2.5, 5]
    scores_normalized = minmax_scaler.fit_transform(scores_train)
    for i in range(0, len(data)):
        data[i]['score'] = scores_normalized[i][0]
    f.close()

with open ('./final.json', "w") as f:
    json.dump(data, f, indent = 4)

#relevant link: https://scikit-learn.org/stable/modules/preprocessing.html


#################### 2. DELETE DUPLICATE JOKES #########################
joke_list = {}
final = []
with open ('./final.json') as f:
    data = json.load(f)
    for i in range (0, len(data)):
        joke = data[i]['joke']
        if joke not in joke_list.keys():
            joke_list[joke] = len(final)
            final.append(data[i])
        else: 
            duplicate_index = joke_list[joke]
            duplicate_score = 0 if final[duplicate_index]['score'] is None else final[duplicate_index]['score']
            duplicate_categories = final[duplicate_index]['categories']

            curr_score = 0 if data[i]['score'] is None else data[i]['score']
            curr_categories = data[i]['categories']

            new_categories = list(set(duplicate_categories + curr_categories))
            new_score = (duplicate_score + curr_score) / 2

            final[duplicate_index]['categories'] = new_categories
            final[duplicate_index]['score'] = null if new_score is None else new_score
    f.close()

with open ('./final.json', "w") as f:
    json.dump(final, f, indent = 4)