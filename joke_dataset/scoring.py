# run file to normalize or standardize scoring
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import numpy as np
from glob import glob
import json
from pathlib import Path
import os

Path('/root/dir/sub/file.ext').stem

scaler = StandardScaler()
minmax_scaler = MinMaxScaler(feature_range = (2.5, 5))

for filename in glob('./json/data_nopreprocess/*.json'):
    name = Path(filename).stem

    with open(filename) as f:
        data = json.load(f) 
        scores_train = [obj['score'] for obj in data]
        if (scores_train[0] is not None): 
            scores_train = np.array_split(scores_train, len(scores_train))

            # normalize scoring from [min, max] to [2.5, 5]
            scores_normalized = minmax_scaler.fit_transform(scores_train)
            for i in range(0, len(data)):
                data[i]['score'] = scores_normalized[i][0]

            # standardize scoring, then normalize to [2.5, 5]
            # scores_scaled = scaler.fit_transform(scores_train)
            # for i in range(0, len(data)):
            #     data[i]['score'] = scores_scaled[i][0]
        f.close()
    
    path = os.path.join('./json/data_preprocess', name + "." + "json")
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
        f.close()