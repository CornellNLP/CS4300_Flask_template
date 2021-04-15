# make an inverted index where for each it can build in these ways:
# - just reviews
# - reviews and trail descriptions
# - trail attributes
# each term for keys
# and then for the postings have it be term frequency and doc names

class InvertedIndex:

    idx = {}
    # token_type can be {'reviews and descriptions', 'reviews', 'attributes', 'descriptions'}
    def __init__(self, token_type='reviews and descriptions'):
        assert token_type in ['reviews and descriptions', 
                              'reviews', 
                              'attributes', 
                              'descriptions']

        if token_type is 'reviews and descriptions':
            self.idx = self.build_inv_idx_words(descriptions = True)
        elif token_type is 'reviews':
            self.idx = self.build_inv_idx_words()
        elif token_type is 'descriptions':
            self.idx = self.build_inv_idx_words(reviews = False, descriptions = True)
        else:
            self.idx = self.build_inv_idx_attributes()

    def build_inv_idx_words(self, reviews = True, descriptions = False):
        return {}

    def build_inv_idx_attributes(self):
        return {}
