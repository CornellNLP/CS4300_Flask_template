from get_data import data 
import re
from nltk.tokenize import TreebankWordTokenizer

class Tokens:
    """
    Given the token type (default is reviews) it tokenizes the data
    token_type can be either 'reviews and descriptions', 'reviews', 'attributes', or 'descriptions'
    token_object = Token(token_type = 'attributes)
    list of tokens -> token_object.tokens
    dictionary of tokens to index -> token_object.tokens_to_idx
    """

    tokens = []
    tokens_to_idx = None
    
    def __init__(self, token_type='reviews'):
        assert token_type in ['reviews and descriptions', 
                              'reviews', 
                              'attributes', 
                              'descriptions']
        # print(token_type)
        if token_type == 'reviews and descriptions':
            self.tokens = self._get_tokens(descriptions = True)
        elif token_type == 'reviews':
            self.tokens = self._get_tokens()
        elif token_type == 'descriptions':
            self.tokens = self._get_tokens(reviews = False, descriptions = True)
        else:
            self.tokens = self._get_tokens_attributes()
        self.tokens_to_idx = self._build_tokens_to_idx()
        
    def _get_tokens(self, reviews = True, descriptions = False):
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

    def _get_tokens_attributes(self):
        tokens = set()
        for trail in data:
            tokens.update(data[trail]['Trail Attributes'])
        return list(tokens)

    def _build_tokens_to_idx(self):
        tokens_to_index = {}
        for i in range(len(self.tokens)):
            print(self.tokens[i])
            tokens_to_index[self.tokens[i]] = i
        print(tokens_to_index)
        return tokens_to_index

## TEST CODE
# token = Tokens(token_type ='attributes')
# tokens = token.tokens
# print(token.tokens_to_idx['Restrooms available'])

