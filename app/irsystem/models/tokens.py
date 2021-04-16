from get_data import data, trail_to_idx
from nltk.tokenize import TreebankWordTokenizer

class Tokens:
    """
    Given the token type (default is reviews) it tokenizes the data
    token_type can be either 'reviews and descriptions', 'reviews', 'attributes', or 'descriptions'
    token_object = Tokens(token_type = 'attributes)
    list of tokens -> token_object.tokens
    dictionary of tokens to index -> token_object.tokens_to_idx
    list of tokens per trail id -> token_object.tokens_per_trail
    """

    tokens = []
    tokens_per_trail = {}
    tokens_to_idx = None
    
    def __init__(self, token_type='reviews'):
        assert token_type in ['reviews and descriptions', 
                              'reviews', 
                              'attributes', 
                              'descriptions']
        if token_type == 'reviews and descriptions':
            self.tokens_per_trail = self._get_tokens_per_trail(descriptions = True)
        elif token_type == 'reviews':
            self.tokens_per_trail = self._get_tokens_per_trail()
        elif token_type == 'descriptions':
            self.tokens_per_trail = self._get_tokens_per_trail(reviews = False, descriptions = True)
        else:
            self.tokens_per_trail = self._get_tokens_per_trail_attributes()
        self.tokens = self._get_tokens()
        self.tokens_to_idx = self._build_tokens_to_idx()
    
    def _get_tokens_per_trail(self, reviews = True, descriptions = False):
        tokens_per_trail = {}
        tokenize = TreebankWordTokenizer().tokenize
        for i, trail in enumerate(data):
            tokens = []
            if reviews:
                for review in data[trail]['Reviews']:
                    tokens.extend(tokenize(review['comment'].lower()))
            if descriptions:
                tokens.extend(tokenize(data[trail]['Description'].lower()))
            tokens_per_trail[i] = tokens
        return tokens_per_trail
    
    def _get_tokens_per_trail_attributes(self):
        tokens_per_trail = {}
        for i, trail in enumerate(data):
            tokens_per_trail[i] = list(set(data[trail]['Trail Attributes']))
        return tokens_per_trail

    def _get_tokens(self, reviews = True, descriptions = False):
        tokens = set()
        for trail in self.tokens_per_trail:
            tokens_of_trail = self.tokens_per_trail[trail]
            tokens.update(tokens_of_trail)
        return list(tokens)

    def _build_tokens_to_idx(self):
        tokens_to_index = {}
        for i in range(len(self.tokens)):
            tokens_to_index[self.tokens[i]] = i
        return tokens_to_index

## TEST CODE
# tokens_obj = Tokens(token_type='attributes')
# tokens_per_trail = tokens_obj.tokens_per_trail
# print(trail_to_idx)
# print(token._get_tokens_per_trail()[1])
# print(tokens_per_trail[trail_to_idx['Ellis Hollow Red trail']] == tokens_per_trail[1])
# print(tokens_per_trail[1])
# print(token.tokens)
# print(len(token.tokens))
# print(token.tokens_to_idx['Restrooms available'])

