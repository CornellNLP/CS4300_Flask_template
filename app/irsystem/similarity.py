import re
import numpy as np
import pandas as pd
import pickle
import json
from nltk.tokenize import TreebankWordTokenizer
import collections
import math

transcripts = pd.read_csv('ted-talks/transcripts.csv')
talk_information = pd.read_csv('ted-talks/ted_main.csv')

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

all_words_total = tokenize_transcript(tokenize,talk_information['description'])

description_word_dict = (collections.Counter(all_words_total))
good_types_descriptions = {k:v for (k,v) in description_word_dict.items() if (v != 0)}

all_words_total_transcripts = tokenize_transcript(tokenize, transcripts['transcript'])
transcript_word_dict = (collections.Counter(all_words_total_transcripts))
good_types_transcripts = {k:v for (k,v) in transcript_word_dict.items() if (v!=0)}

def compute_idf(doc_freq, n_docs, min_df=1, max_df_ratio=0.95):
    """Returns a dictionary of IDFs for each word
    Params: {doc_freq: Dictionary,
             n_docs: Int}
    Returns: Dictionary
    """
    q = {}
    temp = 0
    for term in doc_freq.keys():
        temp = doc_freq[term]
        if temp >= min_df and temp <= n_docs * max_df_ratio:
            q[term] = math.log(n_docs/(1+temp),2)
    return q

description_idf = compute_idf(good_types_descriptions,len(good_types_descriptions.keys()))
transcript_idf = compute_idf(good_types_transcripts,len(good_types_transcripts.keys()))

def compute_inv(tokenize_method,input_transcript,t_idf):
    q = {}
    for i in (range(0,len(input_transcript))):
        final_lst = tokenize_method(input_transcript[i])
        df_temp = (collections.Counter(final_lst))
        trans_df = {k:v for (k,v) in df_temp.items() if (v != 1)}
        temp = {}
        for term in trans_df.keys():
            if term in t_idf.keys():
                if temp.get(term) == None:
                    temp[term] = 1
                else:
                    temp[term] += 1
        for k in temp.keys():
            if q.get(k) == None:
                q[k] = [(i,temp[k])]
            else:
                q[k].append((i,temp[k]))
    return q


description_inv = compute_inv(tokenize,talk_information['description'],description_idf)
transcript_inv = compute_inv(tokenize,transcripts['transcript'],transcript_idf)

def compute_doc_norms(index, idf, n_docs):
    d = {}
    for k in index.keys():
        for t in index[k]:
            if idf.get(k) != None:
                if d.get(t[0]) == None:
                    d[t[0]] = (t[1] * idf[k])**2
                else:
                    d[t[0]] += (t[1] * idf[k])**2
    for doc in d.keys():
        d[doc] = math.sqrt(d[doc])
    return d

description_norms = compute_doc_norms(description_inv, description_idf, len(description_inv))
transcript_norms = compute_doc_norms(transcript_inv, transcript_idf, len(transcript_inv))

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
    
