import rankings
from cosinesim import getwords, build_vectorizer

data = rankings.data

#load the vectorizer
with open('vectorizer.pickle') as v:
  tfidf_vec = pickle.load(v)

index_to_vocab = {i:v for i, v in enumerate(tfidf_vec.get_feature_names())} #from class
vocab_to_index = {v: i for i, v in index_to_vocab.items()}

def filterRestaurants(price_query, cuisine_query):
  """Returns a new list containing the indices of only restaurants that match the
  user's cuisine and price preferences

  Params: {price_query: string,
            cuisine_query: string
            data: dictionary
            }
  Returns: list
  """
  new_restaurant_indices = [] #list keeping track of all the indices of filtered restaurants
  restaurants = data["BOSTON"]
  for name in restaurants:
    price = int(name["price"])
    cuisine = name["categories"]
    if ((max_price == "low") and (price <= 1)) or ((max_price == "medium") and (price <= 3)) or ((max_price == "high") and (price <= 5)):
      if cuisine_query in cuisine:
        new_restaurant_indices.append(rankings.restaurant_to_index[name]) #add index to list of filtered restaurants
  return new_restaurants_indices

def get_cos_sim(old_review_index, new_review_vector, new_review_norm, input_doc_mat):
  """Returns the cosine similarity of two restaurants.
  
  Params: {old_review_index: int,
            new_review_vector: np.ndarray,
            new_review_norm: int,
            input_doc_mat: np.ndarray,
            }
  Returns: Float 
  """
  #get indicies of movie1 and movie2 and get their tf-idf vectors
  #mov1_index = movie_name_to_index[mov1]
  #mov2_index = movie_name_to_index[mov2]
  #mov1_vector = input_doc_mat[mov1_index]
  old_review_vector = input_doc_mat[old_review_index]
  #get dot product of the vectors
  dot = np.dot(new_review_vector, old_review_vector)
  #get norms of both vectors
  old_review_norm = np.linalg.norm(mov2_vector)
  denom = new_review_norm * old_review_norm
  return dot/denom


def computeCosine(review, filter_restaurants, tfidf_mat):
  """Returns a matrix of size 1 x number of reviews total, where entry
  matrix[i] is the cosine similarity between the new review and review [i]
  Params: {
    review: string
    filter_restaurants: list
    tfidf_mat: np.ndarray
    data: dictionary
  }
  Returns: np.ndarray
  """
  all_words = getwords(review)
  stem_text = [stemmer.stem(t.lower()) for t in all_words if bool(re.match(r"^[a-zA-Z]+$", t))]
  """
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
  #build the tf-idf vector for the new review
  for word in tf_dic:
    word_index = vocab_to_index[word]
    idf = 1/df[word_index]
    tf = tf_dic[word]
    review_vector[word_index] = tf/idf
  
  #compute the norm of the review
  """
  #convert reviews to a vector
  review_vector = tfidf_vec.transform(stem_text).toarray()
  review_norm = np.linalg.norm(review_vector)
  
  #calculate the cos similarities between new review and other restaurants
  cos_similarities = np.zeros(len(data["BOSTON"])*2) #initialize an np array to
                                              #size=number of reviews (2 per restaurant)
  for res_index in restaurants:
    res_name = rankings.index_to_restaurant[res_index]
    #get the reviews corresponding to that restaurant
    review_ids = rankings.review_idx_for_restaurant[res_name]
    for rev in review_ids:
      cos_sim = get_cos_sim(rev_index, review_vector, review_norm, tfidf_mat)
      cos_similarities[rev_index] = res_index
  return cos_similarities

def getCosineRestaurants(review, filter_restaurants):
  """Returns a np array where np[i] is the cosine similarity between the new
  review and restaurant i
  Params: {
    review: string
    filter_restaurants: list (of only the relevant restaurants/ones that fit the query)
  }
  """
  tfidf_mat = np.array(np.load('tfidfmat.npy'))
  #compute the cosine similarities between new review and the relevant old reviews
  review_cosines = computeCosine(review, filter_restaurants, tfidf_mat)

  #initialize a numpy array of size = number of restaurants
  restaurant_cosines = np.zeros(len(data["BOSTON"]))
  for res in filter_restaurants:
    res_name = rankings.index_to_restaurant[res]
    review_ids = rankings.review_idx_for_restaurant[res_name]
    val1 = review_cosines[review_ids[0]]
    val2 = review_cosines[review_ids[1]]
    avg = (val1 + val2)/2
    #update the cosine sim for the restaurant
    restaurant_cosines[res] = avg

  return restaurant_cosines
