import rankings
from cosinesim import getwords, build_vectorizer

def filterRestaurants(price_query, cuisine_query, data):
  #returns a new list containing the indices of only restaurants that match the
  #user's cuisine and price preferences
  new_restaurant_indices = [] #list keeping track of all the indices of filtered restaurants
  restaurants = data["BOSTON"]
  for name in restaurants:
    price = int(name["price"])
    cuisine = name["categories"]
    if ((max_price == "low") and (price <= 1)) or ((max_price == "medium") and (price <= 3)) or ((max_price == "high") and (price <= 5)):
      if cuisine_query in cuisine:
        new_restaurant_indices.append(restaurant_to_index[name]) #add index to list of filtered restaurants
  return new_restaurants_indices

def get_cos_sim(res2_index, res1_vector, res1_norm, input_doc_mat):
  """Returns the cosine similarity of two movie scripts.
  
  Params: {mov1: String,
            mov2: String,
            input_doc_mat: np.ndarray,
            movie_name_to_index: Dict}
  Returns: Float 
  """
  #get indicies of movie1 and movie2 and get their tf-idf vectors
  #mov1_index = movie_name_to_index[mov1]
  #mov2_index = movie_name_to_index[mov2]
  #mov1_vector = input_doc_mat[mov1_index]
  res2_vector = input_doc_mat[res2_index]
  #get dot product of the vectors
  dot = np.dot(res1_vector, res2_vector)
  #get norms of both vectors
  mov2_norm = np.linalg.norm(mov2_vector)
  denom = mov1_norm * mov2_norm
  return dot/denom


def computeCosine(review, filter_restaurants, tfidf_mat, data):
  """Returns a matrix of size 1 x number of restaurants total, where entry
  matrix[i] is the cosine similarity between the new review and 
  """

  tfidf_vec = build_vectorizer()
  index_to_vocab = {i:v for i, v in enumerate(tfidf_vec.get_feature_names())} #from class
  vocab_to_index = {v: i for i, v in index_to_vocab.items()}
  all_words = getwords(review)
  stem_text = [stemmer.stem(t.lower()) for t in all_words if bool(re.match(r"^[a-zA-Z]+$", t))]
  #create a dic with keys = each word in the review and values = tf of that word
  tf_dic = {}
  for word in stem_text:
    if word in tf_dic:
      tf_dic[word] += 1
    else:
      tf_dic[word] = 1

  vocab_size = len(vocab_to_index.get_feature_names())
  df = np.sum(tfidf_mat,axis=0) #how to get the doc frequencies of each word?
  
  #initialize the tfidf vector and the norm for this review
  review_vector = np.zeros(vocab_size)
  review_norm = np.linalg.norm(review_vector)
  #build the tf-idf vector for the new review
  for word in tf_dic:
    word_index = vocab_to_index[word]
    idf = 1/df[word_index]
    tf = tf_dic[word]
    review_vector[word_index] = tf/idf
  
  #calculate the cos similarities between new review and other restaurants
  cos_similarities = np.zeros(len(data["BOSTON"]))
  for res_index in restaurants:
    cos_sim = get_cos_sim(res_index, review_vector, review_norm, tfidf_mat)
    cos_similarities[res_index] = res_index
    return cos_similarities

    

