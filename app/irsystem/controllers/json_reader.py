# Module for reading json files

import json
import pandas as pd
import numpy as np


def json_read(file_name):
    """
    Takes a file_path for a json file and converts into a pandas dataFrame and
    return.
    """
    with open(file_name) as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    return df


def json_read_vector(file_name):
    """
    Takes a file_path for a json file of type wine_variety_vectors.json and
    returns a legend where legend[i] is the personality trait being described
    at position i, index where index[i] is the wine variety being described at
    position i, and a matrix where matrix[i][j] is the magnitude of personality
    type j in wine i.
    """
    with open(file_name) as f:
        data = json.load(f)
    legend = data["legend"]
    vectors = data["data"]
    wine_personality_matrix = np.zeros((len(vectors), len(legend)))
    index = []
    for count, i in enumerate(vectors):
        index.append(i["variety"])
        wine_personality_matrix[count] = i["personality_vector"]
    return legend, index, wine_personality_matrix
