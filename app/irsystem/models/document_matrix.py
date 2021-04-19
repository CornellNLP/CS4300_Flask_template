import sys
import numpy as np
from app.irsystem.models.inverted_index import InvertedIndex
from collections import Counter
from app.irsystem.models.get_data import data, trail_to_idx
from app.irsystem.models.tokens import *
from sklearn.feature_extraction.text import TfidfVectorizer


class DTMat:
    """
    Inputs:
        - [term_rep], a choice of representations:
            - 'tfidf' (default)
            - 'tf'
            - 'binary'
          This parameter determines the weight of each term in a document's
          vector representation.
        - [token_type], a choice of source for tokens:
            - 'reviews and descriptions'
            - 'reviews'
            - 'attributes'
            - 'descriptions'
          This parameter determines which tokens the Document-Term Matrix
          takes into account.
        - [features] the number of features (aka columns) that the document
          term matrix should have.

    Outputs:
        Creates a document-term matrix object [dtm] with attributes:
        - A numpy array of size [(# trails in the data) x (# features)]
            [mat] -> dtm.mat
        - A string representing the term representation (or weights)
            [term_rep] -> dtm.term_rep
        - A string representing the source type for token retrieval
            [token_type] -> dtm.token_type
        - A number representing the number of tokens (aka features)
            [features] -> dtm.features
        - A list of length [features], the tokens that make up the columns in
          [dtm]
            [feature_names] -> dtm.feature_names
        - The number of trails used to calculate the Tokens object
            [num_trails] -> dtm.num_trails
        - Provided by the Tokens object, a dictionary where keys are indexes
          for a particular trail, and values are lists containing the tokens
          returned from calling [Tokens().tokens.per_trail[trail_idx]] for
          some trail_idx
            [toks_per_trials] -> dtm.toks_per_trail

    Note: By default creates a tf-idf vector representation with [feature] features.
    For a document-term matrix with binary weights for k-features, call
    [DTMat("binary", k)].
    """

    mat = None
    term_rep = ''
    token_type = ''
    features = None
    feature_names = []
    num_trails = None
    toks_per_trails = {}

    def __init__(self, term_rep="tfidf", token_type="reviews and descriptions", features=100):
        assert term_rep in ['tfidf', 'tf', 'binary']
        assert token_type in ['reviews and descriptions',
                              'reviews',
                              'attributes',
                              'descriptions']
        self.features = features
        self.term_rep = term_rep
        self.token_type = token_type
        self.toks_per_trails = Tokens(token_type).tokens_per_trail
        self.num_trails = len(self.toks_per_trails)
        if term_rep == "tfidf":
            self.mat = self._get_tfidf_mat(features)
        if term_rep == "tf":
            self.mat = self._get_tf_mat()
        if term_rep == "binary":
            self.mat = self._get_binary_mat()

    # mat[i, j] := the tf-idf measure for the term j in document i
    def _get_tfidf_mat(self, features):
        vectorizer = TfidfVectorizer(
            stop_words='english',
            max_df=0.9,
            min_df=10,
            max_features=features)
        mat = vectorizer.fit_transform(
            [' '.join(self.toks_per_trails[trail])
             for trail in self.toks_per_trails]).toarray()
        self.feature_names = vectorizer.get_feature_names()
        return mat

    # mat[i, j] := the term frequency of the term j in document i
    # Features are not implemented for this matrix, so all terms are
    # weighed and diplayed
    def _get_tf_mat(self):
        toks = Tokens(self.token_type)
        self.feature_names = toks.tokens
        toks_to_idx = toks.tokens_to_idx
        inv_idx = InvertedIndex(
            token_type=self.token_type, vector_type='tf').inv_idx
        mat = np.zeros([self.num_trails, len(toks.tokens)])

        for tok in inv_idx:
            for doc, frequency in inv_idx[tok]:
                tok_idx = toks_to_idx[tok]
                mat[doc, tok_idx] = frequency
        return mat

    # mat[i, j] := 1 if term j in document i | 0 otherwise
    # Features are not implemented for this matrix, so all terms are
    # weighed and displayed
    def _get_binary_mat(self):
        toks = Tokens(self.token_type)
        self.feature_names = toks.tokens
        toks_to_idx = toks.tokens_to_idx
        inv_idx = InvertedIndex(
            token_type=self.token_type, vector_type='binary').inv_idx
        mat = np.zeros([self.num_trails, len(toks.tokens)])

        for tok in inv_idx:
            for doc in inv_idx[tok]:
                tok_idx = toks_to_idx[tok]
                mat[doc, tok_idx] = 1
        return mat


# # For testing
# def test():

#     # tf-idf dtm for each token_type
#     dtm_rev_desc = DTMat()
#     dtm_rev = DTMat(token_type='reviews')
#     dtm_att = DTMat(token_type='attributes')
#     dtm_desc = DTMat(token_type='descriptions')

#     # tf dtm for each token_type
#     tf_dtm_rev_desc = DTMat(term_rep='tf')
#     tf_dtm_rev = DTMat(term_rep='tf', token_type='reviews')
#     tf_dtm_att = DTMat(term_rep='tf', token_type='attributes')
#     tf_dtm_desc = DTMat(term_rep='tf', token_type='descriptions')

#     # binary dtm for each token_type
#     bin_dtm_rev_desc = DTMat(term_rep='binary')
#     bin_dtm_rev = DTMat(term_rep='binary', token_type='reviews')
#     bin_dtm_att = DTMat(term_rep='binary', token_type='attributes')
#     bin_dtm_desc = DTMat(term_rep='binary', token_type='descriptions')

#     # dict of dicts for all combinations of token_types and term_rep
#     test_dict = {
#         'tfidf': {
#             'reviews and descriptions': dtm_rev_desc,
#             'reviews': dtm_rev,
#             'attributes': dtm_att,
#             'descriptions': dtm_desc,
#         },
#         'tf': {
#             'reviews and descriptions': tf_dtm_rev_desc,
#             'reviews': tf_dtm_rev,
#             'attributes': tf_dtm_att,
#             'descriptions': tf_dtm_desc,
#         },
#         'binary': {
#             'reviews and descriptions': bin_dtm_rev_desc,
#             'reviews': bin_dtm_rev,
#             'attributes': bin_dtm_att,
#             'descriptions': bin_dtm_desc,
#         }
#     }

#     print(
#         '————————————————————————————————————————————————————\n'
#         + '————————————————————————————————————————————————————\n'
#         + '                 TEST RESULTS\n'
#         + '————————————————————————————————————————————————————\n'
#         + '————————————————————————————————————————————————————\n'
#     )
#     for term_rep in test_dict:
#         print('starting ' + term_rep + '———————————————————————————————')
#         for token_type in test_dict[term_rep]:
#             print('     starting ' + token_type)
#             dtm = test_dict[term_rep][token_type]
#             print('     ...features: ' + str(len(dtm.feature_names)))
#             # test for correct term representation
#             assert dtm.term_rep == term_rep
#             # test for correct token type
#             assert dtm.token_type == token_type
#             # test for feature names

#             print('     ...' + token_type + ' is good\n\n     -\n')
#         print(term_rep
#               + ' is good'
#               + ' ———————————————————————————————\n\n'
#               )


# if __name__ == '__main__':
#     test()
