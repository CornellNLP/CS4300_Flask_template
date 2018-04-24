from sklearn.feature_extraction.text import TfidfVectorizer
import json
import pickle
from scipy.sparse.linalg import svds
from sklearn.preprocessing import normalize

import numpy as np

class SVD(Object):
    @staticmethod
    # return jsons from startYear and startMonth to endYear and endMonth (inclusive)
    def getJsonFilePaths(startYear, startMonth, endYear, endMonth):
        jsonFiles = []
        year = startYear
        month = startMonth

        while year <= endYear:
            if year == 2017 and month == 8: # for some reason we don't have this json
                continue
            jsonFiles.append("Parsed JSONs/RC_{0}-{1:0>2}.json".format(year,month))
            month += 1
            if month == 13:
                month = 1
                year += 1

        while month <= endMonth and month <= 12:
            if year == 2017 and month == 8: # for some reason we don't have this json
                continue
            jsonFiles.append("Parsed JSONs/RC_{0}-{1:0>2}.json".format(year,month))
            month += 1

        return jsonFiles

    @staticmethod
    def getTermDocMatrix(vectorizer):
        comments = []
        jsonFilePaths = SVD.getJsonFilePaths(2016, 1, 2016, 1)
        for filePath in jsonFilePaths:
            with open(filePath, 'r') as f:
                rawJson = json.load(f)
                comments += [c["body"] for c in rawJson if c["subreddit"] == "IWantToLearn"]

        td_matrix = vectorizer.fit_transform(comments).transpose()
        return td_matrix

    @staticmethod
    def getSVDMatrices(td_matrix):
        words_compressed, _, docs_compressed = svds(td_matrix, k=50)
        docs_compressed = docs_compressed.transpose()
        return words_compressed, docs_compressed

    @staticmethod
    def closest_words(word_in, k, words_compressed, word_to_index, index_to_word):
        if word_in not in word_to_index: return "Not in vocab."
        sims = words_compressed.dot(words_compressed[word_to_index[word_in], :])
        asort = np.argsort(-sims)[:k + 1]
        return [(index_to_word[i], sims[i] / sims[asort[0]]) for i in asort[1:]]


if __name__ == "__main__":
    vectorizer = TfidfVectorizer(stop_words='english', max_df=.7,
                                 min_df=75)
    td_matrix = SVD.getTermDocMatrix(vectorizer)

    #save the term-doc matrix in a file
    np.save("term_doc_matrix.npy", td_matrix)

    words_compressed, docs_compressed = SVD.getSVDMatrices(td_matrix)

    np.save("docs_compressed.npy", docs_compressed)

    # print(words_compressed.shape)
    # print(docs_compressed.shape)

    word_to_index = vectorizer.vocabulary_
    index_to_word = {i: t for t, i in word_to_index.iteritems()}

    word_to_index_file = open("word_to_index.pkl","wb")
    pickle.dump(word_to_index, word_to_index_file)

    index_to_word_file = open("index_to_word.pkl","wb")
    pickle.dump(index_to_word, index_to_word_file)

    words_compressed = normalize(words_compressed, axis=1)

    np.save("words_compressed.npy", words_compressed)

    # print(type(words_compressed))
    # print(words_compressed.dtype)
    # print(type(docs_compressed))
    # print(docs_compressed.dtype)
    # print({k: word_to_index[k] for k in word_to_index.keys()[:10]})

    # print(SVD.closest_words("kids", 10, words_compressed, word_to_index, index_to_word))
