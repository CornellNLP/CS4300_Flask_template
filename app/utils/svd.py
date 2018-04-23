from sklearn.feature_extraction.text import TfidfVectorizer
import json
from scipy.sparse.linalg import svds
from sklearn.preprocessing import normalize


class SVD:
    @staticmethod
    def getTermDocMatrix():
        vectorizer = TfidfVectorizer(stop_words='english', max_df=.7,
                                     min_df=75)

        stop_words = vectorizer.get_stop_words()

        jsonFileName = "Parsed JSONs/RC_2016-01.json"
        with open(jsonFileName, 'r') as f:
            rawJsons = json.load(f)
            td_matrix = vectorizer.fit_transform([c["body"] for c in rawJsons if c["subreddit"] == "IWantToLearn"]).transpose()
            return td_matrix

    def performSVD():
        #since they both use the vectorizer, might be easier to either make this a class var
        #or create the TD matrix and do SVD in the same method?
        vectorizer = TfidfVectorizer(stop_words='english', max_df=.7,
                                     min_df=75)
        #we should probably look into what k value we want to use
        words_compressed, _, docs_compressed = svds(getTermDocMatrix(), k=40)
        docs_compressed = docs_compressed.transpose()
        word_to_index = vectorizer.vocabulary_
        index_to_word = {i:t for t,i in word_to_index.iteritems()}
        words_compressed = normalize(words_compressed, axis = 1)


if __name__ == "__main__":
    print(SVD.getTermDocMatrix())