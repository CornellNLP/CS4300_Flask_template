from glob import glob
from pathlib import Path
import knn_model_1 as knn
import json
import os

Path('/root/dir/sub/file.ext').stem

for filename in glob('../json/data_nopreprocess/*.json'):
  name = Path(filename).stem

  with open(filename) as f:
    data = json.load(f)
  if data[0]['score'] is None:
    jokes = [i['joke'] for i in data]
    probs = knn.get_scoring(jokes)
    for i in range(len(data)):
      data[i]['score'] = probs[i][1]
  
  path = os.path.join('../json/data_nopreprocess', name + '.json')
  with open(path, 'w') as f:
    json.dump(data, f, indent = 4)

    