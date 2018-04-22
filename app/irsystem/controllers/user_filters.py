
def filter_ratings(movie_dict,score_dict, inp, high_val):
    rtn_movie = {}
    rtn_score = {}
    inp_set = set(inp)
    for movie in movie_dict:
        if movie_dict[movie]['rating'].lower() in inp_set:
            rtn_movie[movie] = movie_dict[movie]
            rtn_score[movie] = score_dict[movie] + high_val
    return rtn_movie, rtn_score

def filter_languages(movie_dict,score_dict, inp, high_val):
    rtn_movie = {}
    rtn_score = {}
    inp_set = set(inp)
    for movie in movie_dict:
        if movie_dict[movie]['original_language'].lower() in inp_set:
            rtn_movie[movie] = movie_dict[movie]
            rtn_score[movie] = score_dict[movie] + high_val
    return rtn_movie, rtn_score