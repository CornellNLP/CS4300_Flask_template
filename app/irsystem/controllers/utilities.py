import json

# remove entries from dictionary that do not have specific ratings
def filter_ratings(movie_dict,score_dict, inp, high_val):
    rtn_movie = {}
    rtn_score = {}
    inp_set = set(inp)
    for movie in movie_dict:
        if movie_dict[movie]['rating'].lower() in inp_set:
            rtn_movie[movie] = movie_dict[movie]
            rtn_score[movie] = score_dict[movie] + high_val
    return rtn_movie, rtn_score

# remove entries from dictionary that do not have specific languages
def filter_languages(movie_dict,score_dict, inp, high_val):
    rtn_movie = {}
    rtn_score = {}
    inp_set = set(inp)
    for movie in movie_dict:
        if movie_dict[movie]['original_language'].lower() in inp_set:
            rtn_movie[movie] = movie_dict[movie]
            rtn_score[movie] = score_dict[movie] + high_val
    return rtn_movie, rtn_score

def get_jsons():
    movies_json = json.load(open('app/static/data/movies.json'))
    movie_dict = dict()
    for movie in movies_json:
        movie_dict[movie['id']] = json.load(open('app/static/data/movies/' + movie['id'] + '.json'))
    castCrew_list = []
    keywords_list = []
    ratings_list = []
    languages_list = []
    for movie in movie_dict:
        castCrew_list += ([member['name'] for member in movie_dict[movie]['cast']] + [member['name'] for member in movie_dict[movie]['crew']])
        keywords_list += movie_dict[movie]['keywords']
        ratings_list.append(movie_dict[movie]['rating'])
        languages_list.append(movie_dict[movie]['original_language'])
    castCrew_list = list(set(castCrew_list))
    castCrew_list.sort()
    castCrew_dict = [{'name' : i} for i in castCrew_list]
    keywords_list = list(set(keywords_list))
    keywords_list.sort()
    keywords_dict = [{'name' : i} for i in keywords_list]
    ratings_list = list(set(ratings_list))
    ratings_list.sort()
    ratings_dict = [{'name' : i} for i in ratings_list]
    languages_list = list(set(languages_list))
    languages_list.sort()
    languages_dict = [{'name' : i} for i in languages_list]

    with open('app/static/data/cast.json', 'w') as outfile:
        json.dump(castCrew_dict, outfile)

    with open('app/static/data/keywords.json', 'w') as outfile:
        json.dump(keywords_dict, outfile)

    with open('app/static/data/ratings.json', 'w') as outfile:
        json.dump(ratings_dict, outfile)

    with open('app/static/data/languages.json', 'w') as outfile:
        json.dump(languages_dict, outfile)
    

if __name__ == "__main__":
    get_jsons()