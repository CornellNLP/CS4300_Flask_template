import sys
import numpy as np
from collections import Counter
from get_data import data, trail_to_idx
from tokens import *
from sklearn.feature_extraction.text import TfidfVectorizer


class DTMat:
    """
    Inputs:
        - [term_rep], a choice of either 'tfidf' or 'binary' which determines
          the weight of each word in a document's vector representation.
        - [features] the number of features (aka columns) that the document
          term matrix should have.

    Outputs:
        Creates a document-term matrix object [dtm] with fields:
        - A numpy array of size [(# trails in the data) x (# features)].
            [mat] -> dtm.mat
        - A list of length [features], the tokens that make up the columns in 
          [dtm].
            [feature_names] -> dtm.feature_names
        - The number of trails used to calculate the Tokens object.
            [num_trails] -> dtm.num_trails
        - Provided by the Tokens object, a dictionary where keys are indexes
          for a particular trail, and values are lists containing the tokens 
          returned from calling [Tokens().tokens.per_trail[trail_idx]] for 
          some trail_idx.
            [toks_per_trials] -> dtm.toks_per_trail

    Note: By default creates a tf-idf vector representation with 50 features.
    For a document-term matrix where features are the [k]-most-popular
    tokens, call [DTMat("token", k)].
    """

    mat = None
    feature_names = []
    num_trails = None
    toks_per_trails = {}

    def __init__(self, term_rep="tfidf", features=50):
        assert term_rep in ['tfidf', 'binary']
        self.toks_per_trails = Tokens().tokens_per_trail
        self.num_trails = len(self.toks_per_trails)
        if term_rep == "tfidf":
            self.mat = self._get_tfidf_mat(features)
        if term_rep == "binary":
            # Unfinshed and more so inefficient
            self.mat = self._get_binary_mat()

    def _get_tfidf_mat(self, features):
        vectorizer = TfidfVectorizer(
            stop_words='english',
            max_df=0.8,
            min_df=10,
            max_features=features)
        mat = vectorizer.fit_transform(
            # Not sure if I should use join here, seems more expensive to use data directly.
            [' '.join(self.toks_per_trails[trail]) for trail in self.toks_per_trails]).toarray()
        self.feature_names = vectorizer.get_feature_names()
        return mat

    def _get_binary_mat(self):
        toks = Tokens()
        toks_dict = self.toks_per_trails
        # should create Counter object with all tokens for [features]-most-popular terms
        # Unimplemented
        all_toks = toks.tokens
        mat = np.zeros([self.num_trails, len(all_toks)])
        for i, trail in enumerate(self.toks_per_trails):
            for j, tok in enumerate(all_toks):
                if tok in self.toks_per_trails[i]:
                    mat[i, j] = 1
        return mat
