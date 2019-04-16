import re
import numpy as np
import pandas as pd
import pickle
import json
import collections
import math

transcripts = pd.read_csv('transcripts.csv')
talk_information = pd.read_csv('ted_main.csv')

def tokenize(text):
    """Returns a list of words that make up the text.
    
    Note: for simplicity, lowercase everything.
    Requirement: Use Regex to satisfy this function
    
    Params: {text: String}
    Returns: List
    """
    words = re.findall(r"[A-Za-z]+'[a-z]+[[:>:]]|[A-Za-z]+", text.lower())
    return words

def tokenize_transcript(tokenize_method,input_transcript):
    """Returns a list of words contained in an entire transcript.
    Params: {tokenize_method: Function (a -> b),
             input_transcript: Tuple}
    Returns: List
    """
    final_lst = []
    for i in (range(0,len(input_transcript))):
        #print(tokenize_method(input_transcript[i]))
        final_lst = final_lst + list(set(tokenize_method(input_transcript[i])))
    return final_lst

description_idf = pickle.load(open("description_idf.pkl", "rb"))
transcript_idf = pickle.load(open("transcript_idf.pkl", "rb"))

description_inv = pickle.load(open("description_inv.pkl", "rb"))
transcript_inv = pickle.load(open("transcript_inv.pkl", "rb"))

description_norms = pickle.load(open("description_norms.pkl", "rb"))
transcript_norms = pickle.load(open("transcript_norms.pkl", "rb"))

def index_search(query, index, idf, doc_norms, tokenize_method):
    _id = 0
    ret = []
    _id_ref = {}
    temp = list(doc_norms.keys())
    while _id < len(temp):
        _id_ref[temp[_id]] = _id
        ret.append((0,temp[_id]))
        _id += 1
        
    q = tokenize_method(query.lower())
    q_comp = {}
    for w in q:
        if q_comp.get(w) == None:
            q_comp[w] = 1
        else:
            q_comp[w] += 1
    q_norm = 0
    for k in q_comp.keys():
        if idf.get(k) != None:
            q_norm += (q_comp[k] * idf[k])**2
    q_norm = math.sqrt(q_norm)
    
    for w in q:
        if idf.get(w) != None and index.get(w) != None:
            for ent in index[w]:
                ret[_id_ref[ent[0]]] = (ret[_id_ref[ent[0]]][0] + q_comp.get(w) * idf.get(w) * ent[1] * idf.get(w), ret[_id_ref[ent[0]]][1])
    _id = 0
    while _id < len(temp):
        if q_norm * doc_norms[temp[_id]] != 0:
            ret[_id] = (ret[_id][0] / (q_norm * doc_norms[temp[_id]]), ret[_id][1])
        _id += 1
        
    ret = sorted(ret,reverse=True)
    return ret


def descrip_search(query):
    #print("Search: "+ query)
    r = index_search(query, description_inv, description_idf, description_norms,tokenize)
    ret = []
    for score, msg_id in r[:10]:
        ret.append([score, talk_information['title'][msg_id], talk_information['description'][msg_id]])
    return ret

def trans_search(query):
    r = index_search(query, transcript_inv, transcript_idf, transcript_norms,tokenize)
    
