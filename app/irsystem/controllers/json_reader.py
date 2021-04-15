# Module for reading json files

import json
import pandas as pd


def json_read(file_name):
    """
    Takes a file_path for a json file and converts into a pandas dataFrame and
    return.
    """
    with open(file_name) as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    return df
