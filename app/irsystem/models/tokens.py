from get_data import data 
import re
from nltk.tokenize import TreebankWordTokenizer

class Tokens:
    tokens = []
    _tokens_to_idx = {}
    
    def __init__(self, token_type='reviews'):
        assert token_type in ['reviews and descriptions', 
                              'reviews', 
                              'attributes', 
                              'descriptions']
        print(token_type)
        if token_type == 'reviews and descriptions':
            self.tokens = self.get_tokens(descriptions = True)
        elif token_type == 'reviews':
            self.tokens = self.get_tokens()
        elif token_type == 'descriptions':
            self.tokens = self.get_tokens(reviews = False, descriptions = True)
        else:
            self.tokens = self.get_tokens_attributes()
        
    def get_tokens(self, reviews = True, descriptions = False):
        tokens = set()
        # tokens2 = set()
        tokenize = TreebankWordTokenizer().tokenize
        for trail in data:
            if reviews:
                for review in data[trail]['Reviews']:
                    tokens.update(tokenize(review['comment'].lower()))
                    # tokens2.update(re.findall('[a-z]+', review['comment'].lower()))
            if descriptions:
                # tokens2.update(re.findall('[a-z]+', data[trail]['Description'].lower()))
                tokens.update(tokenize(data[trail]['Description'].lower()))
        return list(tokens)

    def get_tokens_attributes(self):
        tokens = set()
        for trail in data:
            tokens.update(data[trail]['Trail Attributes'])
        return list(tokens)

    def _build_tokens_to_idx(self):
        tokens_to_index = {}
        for i in range(len(self.tokens)):
            tokens_to_index[self.tokens[i]] = i
        self._tokens_to_idx = tokens_to_index

    def idx(self, token):
        if self._tokens_to_idx is None:
            self._build_tokens_to_idx()
        return self._tokens_to_idx[token]

tokens = Tokens(token_type ='attributes').tokens
print(tokens)
print(len(tokens))
