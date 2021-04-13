"""
OVERALL INPUT: 
    food_words for one movie (query) 
    {movie_title_1: [word_1, word_2, word_3, ...],
     movie_title_2: [word_1, word_2, word_3, ...],
     ...
    }
    
    recipe_list
    [recipe_title1, recipe_title2, recipe_title3, ...]

OVERALL OUTPUT:
    matrix, with movies as rows, recipes as columns, similarity score for each entry
    ex: movie_i and recipe_j similarity is at matrix[i, j]
"""
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# tokenize recipe titles
# output: [{'toks': ['a', 'b']}, {'toks': ['a', 'b']}]
# We have attached a tokenize method that you should use below:
def tokenize(text):
    """Returns a list of words that make up the text.    
    Params: {text: String}
    Returns: Array
    """
    return [x for x in re.findall(r"[a-z]+", text.lower())]


# recipe_list = ["recipe a", "recipe b"]  
# list of recipe titles
def tokenize_titles(recipe_list):
    res = []
    for recipe in recipe_list:
        res.append(tokenize(recipe))
    return res


def build_inverted_index(titles):
    """ Builds an inverted index from the messages.
    
    Arguments
    =========
    
    titles: tokenized recipe titles
    
    Returns
    =======
    
    inverted_index: dict
        For each term, the index contains 
        a sorted list of tuples (doc_id, count_of_term_in_doc)
        such that tuples with smaller doc_ids appear first:
        inverted_index[term] = [(d1, tf1), (d2, tf2), ...]
        
    Example
    =======
    
    >> test_idx = build_inverted_index([
    ...    {'toks': ['to', 'be', 'or', 'not', 'to', 'be']},
    ...    {'toks': ['do', 'be', 'do', 'be', 'do']}])
    
    >> test_idx['be']
    [(0, 2), (1, 2)]
    
    >> test_idx['not']
    [(0, 1)]
    
    Note that doc_id refers to the index of the document/message in msgs.
    """
    # YOUR CODE HERE
    res = defaultdict(list)
    for i in range(len(titles)):
        words = titles[i]
        word_dict = {}
        for word in set(words):
            res[word] += [(i, words.count(word))]
    return res


def build_vectorizer(recipe_list):
    """Returns a TfidfVectorizer object with certain preprocessing properties.
    
    Params: {max_n_terms: Integer,
             max_prop_docs: Float,
             min_n_docs: Integer}
    Returns: matrix, TfidfVectorizer
    """
    # YOUR CODE HERE
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_mat = vectorizer.fit_transform(recipe_list).toarray()
    return tfidf_mat, vectorizer


def get_movie_tfidfs(movie_food_words, vectorizer):
  """
  Params: movie_food_words: 
    {movie_title_1: [word_1, word_2, word_3, ...],
     movie_title_2: [word_1, word_2, word_3, ...],
     ...}

  Returns: List of tfidf vectors for movie food words
  each row is a movie title
  each col is a food word
  """
  queries = []
  for k,v in movie_food_words.items():
    queries.append(" ".join(movie_food_words[k]))
  
  tfidf_mat = vectorizer.transform(queries).toarray()
  return tfidf_mat
    

def get_cos_sim(recipe_mat, movie_mat):
    """Returns the cosine similarity of two movie scripts.
    
    Params: {mov1: String,
             mov2: String,
             input_doc_mat: np.ndarray,
             movie_name_to_index: Dict}
    Returns: Float 
    """

    m = movie_mat.shape[0]
    n = recipe_mat.shape[0]
    res = np.zeros((m,n))
    for i in range(m):
        for j in range(n):
            q = movie_mat[i]
            d = recipe_mat[j]
            numerator = np.dot(q, d)
            denominator = np.dot(np.linalg.norm(q), np.linalg.norm(d))
            res[i,j] = numerator/denominator
    return res


def main():
  #load recipes
  recipe_list = ["Double Cheeseburger", "Cheeseburger Sliders", "Pop-Tarts", "Blueberry Pancakes", "Shrimp and Catfish Gumbo", "Cajun Shrimp", "Shrimp Burgers"]
  #load movie food words
  movie_list = {"Pulp Fiction": ["burger, cheeseburger"], "Forrest Gump": ["shrimp", "chocolates"]}
  recipe_mat, vectorizer = build_vectorizer(recipe_list)
  movie_mat = get_movie_tfidfs(movie_list, vectorizer)
  res = get_cos_sim(recipe_mat, movie_mat)
  print(res)
  return res
  

if __name__ == "__main__":
  main()
  
