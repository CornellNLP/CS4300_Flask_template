from collections import Counter
import pickle
from app.irsystem.models.shared_variables import file_path_name
from app.irsystem.models.shared_variables import num_partitions
from nltk.stem import PorterStemmer

"""
create a class to handle inverted indices (creation & execution)

Attributes:
"""
class InvertedIndex():
    def __init__(self):
        self.inverted_indices = [None for _ in range(num_partitions)]
        self._inverted_index_helper = {}
        print("initialized inverted index")

    stemmer=PorterStemmer()
    def getStem(tokens):
        return [stemmer.stem(word) for word in tokens]

    

    def create(self, data):
        print("...creating inverted index")
        inverted_indices = [{} for _ in range(num_partitions)] #create <partitions> inverted indices
        next_inverted_index = 0 #start at the first one
        inverted_index_helper = {} #tells me which inverted index the item is in

        num_posts = len(data)

        for post in data:
            words = post['tokens']
            wordsstem = getStem(post['tokens'])
            print(len(word))
            print(len(wordsstem))
            count = Counter(words) #count frequency of each word
            for word, frequency in count.most_common():
                if not word in inverted_index_helper:
                    inverted_index_helper[word] = next_inverted_index
                    next_inverted_index = (next_inverted_index + 1)  % num_partitions
                    inverted_indices[inverted_index_helper[word]][word] = [] 
                inverted_index = inverted_indices[inverted_index_helper[word]]
                inverted_index[word].append((post['id'], frequency))
        self.inverted_indices = inverted_indices
        self._inverted_index_helper = inverted_index_helper
        

    def store(self):
        for i in range(len(self.inverted_indices)):
            inverted_index = self.inverted_indices[i]
            file = self.create_file_name(i)
            pickle.dump(inverted_index, open(file, 'wb'))
        helper = self.create_file_name("helper")
        pickle.dump(self._inverted_index_helper, open(helper, 'wb'))

    def create_file_name(self, suffix):
        return "{}-inverted_index-{}.pickle".format(file_path_name, str(suffix))

    def load_file(self, file_suffix):
        print("...loading " + self.create_file_name(file_suffix))
        with open(self.create_file_name(file_suffix), 'rb') as file:
            return pickle.load(file)

    #will load based on information in shared_variables
    #only load helper first, load everything else as needed
    def load(self):
        # for partition_index in range(num_partitions):
        #     inverted_index = self.load_file(partition_index)
        #     self.inverted_indices.append(inverted_index)
        self._inverted_index_helper = self.load_file("helper")

    def get_posts(self, token):
        self.load_by_token(token)
        if token in self._inverted_index_helper:
            inverted_index = self._get_inverted_index(token)
            return inverted_index[token]
        raise KeyError()

    def load_by_token(self, token):
        if token in self._inverted_index_helper:
            inverted_index_i = self._inverted_index_helper[token]
            if self.inverted_indices[inverted_index_i] is None: #haven't loaded this index yet
                self.inverted_indices[inverted_index_i] = self.load_file(inverted_index_i)

    def _get_inverted_index(self, token):
        return self.inverted_indices[self._inverted_index_helper[token]]

    def keys(self):
        return list(self._inverted_index_helper.keys())

    def remove_token(self, token):
        self.load_by_token(token)
        inverted_index = self._get_inverted_index(token)
        del inverted_index[token]
        del self._inverted_index_helper[token]

    def __contains__(self, key):
        return key in self._inverted_index_helper

    def __getitem__(self, key):
        return self.get_posts(key)

    def items(self):
        keys = self.keys()
        return [(key, self.get_posts(key)) for key in keys]

    def __str__(self):
        return str(self.items())
