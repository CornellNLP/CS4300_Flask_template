from .database import query_drink, query_embeddings, query_drink_vbytes
from scipy.spatial.distance import cdist
import numpy as np
import json

class Args:
    def __init__(self, data, dtype, pmin, pmax, amin, amax, base):
        self.data = data # str or list
        self.dtype = dtype # str
        self.pmin = pmin # float
        self.pmax = pmax # float
        self.amin = amin # float
        self.amax = amax # float
        self.base = base # str

    def __eq__(self, value):
        if isinstance(value, Args):
            return self.__dict__ == value.__dict__
        return NotImplemented

def search_drinks(drinks, args):
    query = None
    count = len(drinks)

    # Fetch query vector from drink name
    if type(args.data) == str:
        vbytes = query_drink_vbytes(args.data)
        if vbytes is None:
            return []
        query = np.array(json.loads(vbytes))
    # Form query vector from word embeddings
    if type(args.data) == list:
        emb_dict = {e.word: np.array(json.loads(e.vbytes)) for e in query_embeddings()}
        q_vectors = [emb_dict[d] for d in args.data if d in emb_dict]
        query = sum(q_vectors) / len(q_vectors)

    if query is None:
        return [(d, 0) for d in drinks]

    # Search database results for k nearest neighbors
    d_vectors = [np.array(json.loads(d.vbytes)) for d in drinks]
    knn_data = np.array(d_vectors).reshape(count, -1)
    dst_vec = cdist([query], knn_data, 'cosine')[0]
    ind_vec = np.argsort(dst_vec)
    
    return [(drinks[i], dst_vec[i]) for i in ind_vec if dst_vec[i] <= 0.3]
