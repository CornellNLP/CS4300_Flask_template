from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import json
import math
import user_duration
import user_release
import boosting
import utilities
from random import *

movies_json = json.load(open('app/static/data/movies.json'))

# map each movie id to the movie's information
movie_dict = dict()
for movie in movies_json:
    movie_dict[movie['id']] = json.load(open('app/static/data/movies/' + movie['id'] + '.json'))

# get list of movie titles
movie_list = [movie['title'] for movie in movies_json]
movie_list.sort()

# build other lists from movie_dict
castCrew_list = []
keywords_list = []
ratings_list = []
languages_list = []
max_tmdb_count = 0.0
max_imdb_count = 0.0
max_meta_count = 0.0

for movie in movie_dict:
    castCrew_list += ([member['name'] for member in movie_dict[movie]['cast']] + [member['name'] for member in movie_dict[movie]['crew']])
    keywords_list += movie_dict[movie]['keywords']
    ratings_list.append(movie_dict[movie]['rating'])
    languages_list.append(movie_dict[movie]['original_language'])
    if movie_dict[movie]['tmdb_score_count'] > max_tmdb_count:
        max_tmdb_count = movie_dict[movie]['tmdb_score_count']
    if movie_dict[movie]['imdb_score_count'] > max_imdb_count:
        max_imdb_count = movie_dict[movie]['imdb_score_count']
    if movie_dict[movie]['meta_score_count'] > max_meta_count:
        max_meta_count = movie_dict[movie]['meta_score_count']
castCrew_list = list(set(castCrew_list))
castCrew_list.sort()
keywords_list = list(set(keywords_list))
keywords_list.sort()
ratings_list = list(set(ratings_list))
languages_list = list(set(languages_list))

# get list of years
year_list = range(1900, 2019)

@irsystem.route('/', methods=['GET'])
def search():
    output_message = ""
    data = []
    query_dict = {}

    # user inputs
    similar = request.args.get('similar')
    genres = request.args.get('genres')
    castCrew = request.args.get('castCrew')
    keywords = request.args.get('keywords')
    duration = request.args.get('duration')
    release_start = request.args.get('release_start')
    release_end = request.args.get('release_end')
    ratings = request.args.get('ratings')
    languages = request.args.get('languages')
    acclaim = request.args.get('acclaim')
    popularity = request.args.get('popularity')

    if not acclaim and not popularity:
        data = []
        output_message = ''
    else:
        data = []
        movie_dict = dict()
        score_dict = dict()

        for movie in movies_json:
            movie_dict[movie['id']] = json.load(open('app/static/data/movies/' + movie['id'] + '.json'))
            score_dict[movie['id']] = 0.0
        reverse_dict = {y['title'].lower():x for x,y in movie_dict.iteritems()}


        ########### MESSAGE UPDATE, QUERY DICT GENERATION ###########
        if similar:
            selected_movies = parse_lst_str(similar)
            output_message += "Similar: " + similar + "\n"
        if genres:
            selected_genres = parse_lst_str(genres)
            print selected_genres
            output_message += "Genres: " + genres + "\n"
            query_dict['genres'] = selected_genres
        if castCrew:
            selected_crew = parse_lst_str(castCrew)
            output_message += "Cast and Crew: " + castCrew + "\n"
            query_dict['castCrew'] = selected_crew
        if keywords:
            selected_keywords = parse_lst_str(keywords)
            output_message += "Keywords: " + keywords + "\n"
            query_dict['keywords'] = keywords
        if duration:
            output_message += "Duration: " + duration + "\n"
            duration_val = user_duration.parse(duration)
            duration_val == duration_val[0] if len(duration_val) == 1 else (duration_val[0] + duration_val[1])/2 
            query_dict['runtime'] = duration_val
        if release_start or release_end:
            if release_start and release_end:
                output_message += "Release: " + release_start + "-" + release_end + "\n"
                # query_dict['release_date'] = (release_start + release_end)/2
            elif release_start:
                output_message += "Release: " + release_start + "-2018\n"
            else:
                output_message += "Release: 1900-" + release_end + "\n"
        if ratings:
            selected_ratings = parse_lst_str(ratings)
            output_message += "Ratings: " + ratings + "\n"
        if languages:
            selected_languages = parse_lst_str(languages)
            output_message += "Languages: " + languages + "\n"
        if acclaim == "yes":
            output_message += "Acclaim: Yes\n"
        else:
            output_message += "Acclaim: No\n"
        if popularity == "yes":
            output_message += "Popularity: Yes\n"
        else:
            output_message += "Popularity: No\n"

        ########### BOOST THE "QUERY MOVIE" WITH THE SIMILAR MOVIES ###########
        # must do before filtering because similar movies might be filtered out
        if similar:
            query_dict = boosting.boost_query(query_dict,selected_movies,movie_dict)
            movie_dict,score_dict = utilities.filter_similar(movie_dict,score_dict,selected_movies)

        ########### FILTERING OF DICTIONARIES ###########
        # updates dicts with hard filters
        # for duration and release, also computes scores
        if duration:
            movie_dict, score_dict = user_duration.main(movie_dict,score_dict,duration,0,1)
            duration_score = boosting.gaussian_score_duration(movie_dict,query_dict['runtime'],1,0)
        if release_start or release_end:
            movie_dict, score_dict = user_release.main(movie_dict,score_dict,[release_start, release_end], 0, 1)
        if ratings:
            movie_dict, score_dict = utilities.filter_ratings(movie_dict, score_dict, selected_ratings, 1)
        if languages:
            movie_dict, score_dict = utilities.filter_languages(movie_dict, score_dict, selected_languages, 1)

        ########### VECTORIZE MOVIES GIVEN QUERY ###########
        mod_movie_dict,mod_movie_lst,movieid_lookup = {},[],{}
        # release_score = boosting.gaussian_score_release(movie_dict,query_dict['release_date'],1,0)
        
        counter = 0
        for movie in movie_dict:
            tmp = []
            # list of genres for movie m -> jaccard sim with query
            if genres:
                #mod_movie_dict[movie]['genres'] = get_set_overlap(query_dict['genres'],movie_dict[movie]['genres'])
                tmp.append(get_set_overlap(query_dict['genres'],movie_dict[movie]['genres']))

            # list of cast and crew for movie m -> jaccard sim with the query
            if castCrew:
                cast = [member['name'] for member in movie_dict[movie]['cast']]
                crew = [member['name'] for member in movie_dict[movie]['crew']]
                #mod_movie_dict[movie]['castCrew'] = get_set_overlap(selected_crew, cast + crew)
                tmp.append(get_set_overlap(selected_crew, cast + crew))

            # keywords from query -> jaccard sim with the movie m synopsis
            if keywords:
                #mod_movie_dict[movie]['keywords'] = get_set_overlap(selected_keywords, movie_dict[movie]['keywords'])
                tmp.append(get_set_overlap(selected_keywords, movie_dict[movie]['keywords']))

            # duration & release date from movie m -> probabilistic gaussian fit around the mean 
            if duration:
                duration_val = duration_score[movie][0]
                #mod_movie_dict[movie]['runtime'] = duration_val
                tmp.append(duration_val)

            # TODO: implement release date into calculation later
            #mod_movie_dict[movie]['release_date'] = release_score[movie]
            #tmp.append(duration_score[movie])

            # clean-up...
            mod_movie_lst.append(tmp)
            movieid_lookup[counter] = movie
            counter += 1

            # TODO: incorporate acclaim and popularity into score...


        mod_movie_mat = np.zeros((len(mod_movie_lst),len(mod_movie_lst[0])))
        for i in range(len(mod_movie_lst)):
            for k in range(len(mod_movie_lst[i])):
                mod_movie_mat[i][k] = mod_movie_lst[i][k]

        ########### RUN KNN ON VECTORS, RETURN TOP MATCHES ###########

        n,d = mod_movie_mat.shape
        query = np.ones(d)
        dists = np.linalg.norm(mod_movie_mat - query,axis=1,ord=2)
        #print(movie_dict.keys())
        #print("here is your dists matrix ")
        #print(dists)
        #print()
        ranked_lst = np.argsort(dists)

        #print(ranked_lst)

        print("movie_id lookup dictionary")
        print(movieid_lookup)

        
        sorted_score_dict = [movieid_lookup[movie_id] for movie_id in ranked_lst]

        for movie_id in sorted_score_dict:
            #dt = datetime.datetime.strptime(movie_dict[movie_id]['release_date'], '%Y-%m-%d').strftime('%m-%d-%Y')
            #movie_dict[movie_id]['release_date'] = dt
            data.append(movie_dict[movie_id])


        data = [data[i:i + 4] for i in xrange(0, len(data), 4)]

    return render_template('search.html',
        old_similar = xstr(similar),
        old_genres = xstr(genres),
        old_castCrew = xstr(castCrew),
        old_keywords = xstr(keywords),
        old_duration = xstr(duration),
        old_release_start = xstr(release_start),
        old_release_end = xstr(release_end),
        old_ratings = xstr(ratings),
        old_languages = xstr(languages),
        old_acclaim = xstr(acclaim),
        old_popularity = xstr(popularity),
        output_message= output_message,
        data = data[:24],
        movie_list = movie_list,
        castCrew_list = castCrew_list,
        keywords_list = keywords_list,
        year_list = year_list)

def parse_lst_str(lst_str):
    parsed = []
    if lst_str:
        lst_str = lst_str.encode('ascii', 'ignore')
        if ';' in lst_str:
            parsed = lst_str.split(";")
        else:
            parsed = [lst_str]
        for ind in range(0, len(parsed)):
            parsed[ind] = parsed[ind].lower().strip()
    return parsed

# get the fraction of items in list1 available in list2
def get_set_overlap(list1, list2):
    set1 = set([x.lower() for x in list1])
    set2 = set([x.lower() for x in list2])
    num = float(len(set1.intersection(set2)))
    den = len(set1)
    return num / den

def xstr(s):
    return '' if s is None else str(s)
