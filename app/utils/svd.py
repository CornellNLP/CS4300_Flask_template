from sklearn.feature_extraction.text import TfidfVectorizer
import json
import pickle
from scipy.sparse.linalg import svds
from sklearn.preprocessing import normalize
import numpy as np
from nltk.stem import PorterStemmer

class SVD:
    @staticmethod
    # return jsons from startYear and startMonth to endYear and endMonth (inclusive)
    def getJsonFilePaths(startYear, startMonth, endYear, endMonth):
        jsonFiles = []
        year = startYear
        month = startMonth

        while year < endYear:
            if year == 2017 and month == 8: # for some reason we don't have this json
                month += 1
                continue
            jsonFiles.append("Parsed JSONs/RC_{0}-{1:0>2}.json".format(year,month))
            month += 1
            if month == 13:
                month = 1
                year += 1

        while month <= endMonth and month <= 12:
            if year == 2017 and month == 8: # for some reason we don't have this json
                month += 1
                continue
            jsonFiles.append("Parsed JSONs/RC_{0}-{1:0>2}.json".format(year,month))
            month += 1

        return jsonFiles

    @staticmethod
    def getTermDocMatrix(vectorizer):
        comments = []
        jsonFilePaths = SVD.getJsonFilePaths(2016, 1, 2018, 1)
        for filePath in jsonFilePaths:
            print("Opening %s" % filePath)
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
    folder = "Matrices"

    print("Getting term doc matrix...")
    td_matrix = SVD.getTermDocMatrix(vectorizer)
    print("Got term doc matrix!")
    print("Saving term doc matrix...")
    np.save(folder + "/term_doc_matrix.npy", td_matrix)
    print("Saved term doc matrix!")

    print("Getting svd matrices..")
    words_compressed, docs_compressed = SVD.getSVDMatrices(td_matrix)
    print("Got svd matrices!")
    print("Saving docs_compressed...")
    np.save(folder + "/docs_compressed.npy", docs_compressed)
    print("Saved docs_compressed!")

    print("Getting word_to_index...")
    word_to_index = vectorizer.vocabulary_
    print("Got word_to_index!")

    print("Getting index_to_word...")
    index_to_word = {i: t for t, i in word_to_index.iteritems()}
    print("Got index_to_word!")

    print("Saving word_to_index...")
    word_to_index_file = open(folder + "/word_to_index.pkl","wb")
    pickle.dump(word_to_index, word_to_index_file)
    print("Saved word_to_index!")

    print("Saving index_to_word...")
    index_to_word_file = open(folder + "/index_to_word.pkl","wb")
    pickle.dump(index_to_word, index_to_word_file)
    print("Saved index_to_word!")

    print("Normalizing words_compressed...")
    words_compressed = normalize(words_compressed, axis=1)
    print("Normalized words_compressed!")
    print("Saving words_compressed...")
    np.save(folder + "/words_compressed.npy", words_compressed)
    print("Saved words_compressed!")

    print({k: word_to_index[k] for k in word_to_index.keys()[:10]})
    print(SVD.closest_words("piano", 10, words_compressed, word_to_index, index_to_word))
