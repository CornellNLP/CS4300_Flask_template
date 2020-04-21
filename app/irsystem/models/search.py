from .database import query_drink, query_embeddings
from sklearn.neighbors import NearestNeighbors
import numpy as np

def search_drinks(descriptors, dtype=None, k=10):
    # Form query vector from word embeddings
    emb_dict = {e.word: np.frombuffer(e.vbytes, dtype=np.float32) for e in query_embeddings()}
    q_vectors = [emb_dict[d] for d in descriptors if d in emb_dict]
    if len(q_vectors) == 0:
        return None
    query = sum(q_vectors) / len(q_vectors)
    
    # Search database for k nearest neighbors
    drinks = query_drink(dtype)
    d_vectors = [np.frombuffer(d.vbytes, dtype=np.float32) for d in drinks]
    knn_data = np.array(d_vectors).reshape(drinks.count(), -1)
    knn = NearestNeighbors(n_neighbors=k, algorithm='auto', metric='cosine')
    model = knn.fit(knn_data)
    dst, ind = model.kneighbors([query])

    # Return list of `(drink, distance)` tuples
    dst_lst = dst[0].tolist()
    ind_lst = ind[0].tolist()
    return [(drinks[i], dst) for (i, dst) in zip(ind_lst, dst_lst)]
