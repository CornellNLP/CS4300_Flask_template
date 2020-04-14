from gensim.models import Word2Vec
from data_tools import get_descriptor, get_wine_data, get_beer_data, tokenize
# from data_tools import get_wine_data
# from data_tools import get_beer_data
# from data_tools import tokenize

def main():
    wine_data = get_wine_data() # Sentence reviews about wines
    wine_types = tokenize(wine_data) # Set of unique types that appear in sentences
    beer_data = get_beer_data()
    beer_types = tokenize(beer_data)

    sentences = [] # placeholder

    norm_sentences = []
    for s in sentences:
        norm_s = []
        for w in s:
            norm_w = get_descriptor(w)
            norm_s.append(norm_w)
        norm_sentences.append(norm_s)

    model = Word2Vec(norm_sentences, size=300, min_count=5, iter=15)

main()
