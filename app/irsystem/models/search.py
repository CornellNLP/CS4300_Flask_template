from .database import query_drink, query_embeddings, query_drink_vbytes
from sklearn.neighbors import NearestNeighbors
import numpy as np

def search_drinks(data, dtype=None, k=10, page=1, pmin=None, pmax=None, amin=None, amax=None, base=None):
    # Fetch query vector from drink name
    if type(data) == str:
        vbytes = query_drink_vbytes(data)
        if vbytes is None:
            return None
        query = np.frombuffer(vbytes, dtype=np.float32)
    # Form query vector from word embeddings
    if type(data) == list:
        emb_dict = {e.word: np.frombuffer(e.vbytes, dtype=np.float32) for e in query_embeddings()}
        q_vectors = [emb_dict[d] for d in data if d in emb_dict]
        if len(q_vectors) == 0:
            return None
        query = sum(q_vectors) / len(q_vectors)
    
    # Search database for k nearest neighbors
    drinks = query_drink(dtype, pmin, pmax, amin, amax, base)
    d_vectors = [np.frombuffer(d.vbytes, dtype=np.float32) for d in drinks]
    if len(d_vectors) == 0:
        return None
    if len(d_vectors) < k:
        k = len(d_vectors)
        if page > 1:
            return None
    knn_data = np.array(d_vectors).reshape(drinks.count(), -1)
    knn = NearestNeighbors(n_neighbors=k*page, algorithm='auto', metric='cosine')
    model = knn.fit(knn_data)
    dst, ind = model.kneighbors([query])

    # Return list of `(drink, distance)` tuples
    dst_lst = dst[0].tolist()[(page-1)*k:]
    ind_lst = ind[0].tolist()[(page-1)*k:]
    return [[drinks[i], dst] for (i, dst) in zip(ind_lst, dst_lst)]
