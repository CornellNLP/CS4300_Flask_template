import pandas as pd

DATA_DIR = 'embeddings/data/'
DESC_MAP = pd.read_csv(DATA_DIR + 'descriptor_mapping.csv').set_index('raw descriptor')

def get_descriptor(word):
    if word in list(DESC_MAP.index):
        norm = DESC_MAP['level_3'][word]
        return norm
    else:
        return word

