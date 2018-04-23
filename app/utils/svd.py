from sklearn.feature_extraction.text import TfidfVectorizer
import json


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


if __name__ == "__main__":
    print(SVD.getTermDocMatrix())