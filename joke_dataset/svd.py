import numpy as np 
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds
import matplotlib
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
from sklearn.manifold import TSNE
from collections import Counter
from collections import defaultdict

with open('./final_score.json') as f:
  data = json.load(f)

vectorizer = TfidfVectorizer(stop_words = 'english', max_df = 0.7, min_df = 75)
mtrx = vectorizer.fit_transform([x['joke'] for x in data]).T 
print(type(mtrx))
print(mtrx.shape)

u, s, v_trans = svds(mtrx, k = 500)

# plt.plot(s[::-1])
# plt.xlabel("Singular value number")
# plt.ylabel('Singular value')
# plt.show()

words_compressed, _, docs_compressed = svds(mtrx, k = 100)
docs_compressed = docs_compressed.T

word_to_index = vectorizer.vocabulary_
# print(word_to_index)
idx_to_wrd = {i:t for t, i in word_to_index.items()}

words_compressed = normalize(words_compressed, axis =1)

def closest_words(word_in, k = 10):
    if word_in not in word_to_index: return "Not in vocab."
    sims = words_compressed.dot(words_compressed[word_to_index[word_in],:])
    asort = np.argsort(-sims)[:k+1]
    return [(idx_to_wrd[i],sims[i]/sims[asort[0]]) for i in asort[1:]]

# print(closest_words('dad'))



tsne = TSNE(verbose = 1)
projected_docs = tsne.fit_transform(docs_compressed)
# plt.figure(figsize = (15, 15))
# plt.scatter(projected_docs[:,0],projected_docs[:,1])
# plt.show()

cats = Counter([i for x in data for i in x['categories']])
print(cats)
cat_to_color = defaultdict(lambda: 'k')
cat_to_color.update({'Biology': 'g',
                    'Heaven and Hell': 'c',
                    'Pun': 'r',
                    'Pick-up Line': 'b'})
color_to_project = defaultdict(list)
for i in range(projected_docs.shape[0]):
  if data[i]['categories'] != []:
    color_to_project[cat_to_color[data[i]['categories'][0]]].append(i)

plt.figure(figsize=(15,15))
for color, indices in color_to_project.items():
    indices = np.array(indices)
    plt.scatter(projected_docs[indices,0], projected_docs[indices,1],
                color = color)
plt.show()