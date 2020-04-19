from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from numpy import linalg as LA
import json
import math
import matplotlib.pyplot as plt
from nltk.tokenize import TreebankWordTokenizer
import re

tokenizer = re.compile(r"[^A-z0-9]*\s+[^A-z0-9]*|\.\s*|'(?=s)[A-z]+\s*|-", re.VERBOSE)
tokenizer = TreebankWordTokenizer()

def tokenize(str):
    toks = tokenizer.split(' ' + str.lower() + ' ')
    return toks[1:len(toks)-1]

def add_tokens(tokenizer, data):
    result = data

    for i in range(len(result)):
        result[i]['toks'] = tokenizer.tokenize(result[i]['joke'].lower())

    return result

def update_json():
    with open("final.json") as f:
        data = json.load(f)

    num_jokes = len(data)
    print("Loaded {} jokes".format(num_jokes))
    print("Each joke has the following keys:")
    print(data[0].keys())

    data = add_tokens(tokenizer, data)

    with open('final_toks.json', 'w') as f:
        json.dump(data, f, indent = 4)
