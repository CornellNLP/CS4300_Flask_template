from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import json
import math
import user_duration
import user_release
import user_filters
from random import *

movies_json = json.load(open('app/static/data/movies.json'))
genres_json = json.load(open('genres.json'))

# map each movie id to the movie's information
movie_dict = dict()
for movie in movies_json:
    movie_dict[movie['id']] = json.load(open('app/static/data/movies/' + movie['id'] + '.json'))

# get list of movie titles
movie_list = [movie['title'] for movie in movies_json]
movie_list.sort()

# get list of genres
genre_list = [genre['name'] for genre in genres_json['genres']]

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

    if not similar and not genres and not duration and not acclaim and not castCrew and not keywords and not release_start and not release_end:
        data = []
        output_message = ''
    else:
        data = []
        max_score = 0.0
        movie_dict = dict()
        score_dict = dict()

        for movie in movies_json:
            movie_dict[movie['id']] = json.load(open('app/static/data/movies/' + movie['id'] + '.json'))
            score_dict[movie['id']] = 0.0
        reverse_dict = {y['title'].lower():x for x,y in movie_dict.iteritems()}


        ########### MESSAGE UPDATE, SCORE ASSIGNMENT ###########
        if similar:
            selected_movies = parse_lst_str(similar)
            output_message += "Similar: " + similar + "\n"
            similar_score = 10.0
            max_score += similar_score
        if genres:
            selected_genres = parse_lst_str(genres)
            output_message += "Genres: " + genres + "\n"
            genres_score = 10.0
            max_score += genres_score
        if castCrew:
            selected_crew = parse_lst_str(castCrew)
            output_message += "Cast and Crew: " + castCrew + "\n"
            castCrew_score = 10.0
            max_score += castCrew_score
        if keywords:
            selected_keywords = parse_lst_str(keywords)
            output_message += "Keywords: " + keywords + "\n"
            keywords_score = 10.0
            max_score += keywords_score
        if duration:
            output_message += "Duration: " + duration + "\n"
            duration_score = 10.0
            max_score += duration_score
        if release_start or release_end:
            if release_start and release_end:
                output_message += "Release: " + release_start + "-" + release_end + "\n"
            elif release_start:
                output_message += "Release: " + release_start + "-2018\n"
            else:
                output_message += "Release: 1900-" + release_end + "\n"
            release_score = 10.0
            max_score += release_score
        if ratings:
            selected_ratings = parse_lst_str(ratings)
            output_message += "Ratings: " + ratings + "\n"
            ratings_score = 10.0
            max_score += ratings_score
        if languages:
            selected_languages = parse_lst_str(languages)
            output_message += "Languages: " + languages + "\n"
            languages_score = 10.0
            max_score += languages_score
        if acclaim == "yes":
            output_message += "Acclaim: Yes\n"
            acclaim_score = 10.0
            max_score += acclaim_score
        else:
            output_message += "Acclaim: No\n"
        if popularity == "yes":
            output_message += "Popularity: Yes\n"
            popularity_score = 10.0
            max_score += popularity_score
        else:
            output_message += "Popularity: No\n"

        ########### CALCULATE SIMILAR SCORE ###########
        # must do before filtering because similar movies might be filtered out
        if similar:
            for movie in score_dict:
                # if the movie is already in the selected_titles
                if movie_dict[movie]['title'].lower() in set(selected_movies):
                    score_dict[movie] -= max_score
                else:
                    cumulative_score = 0.0
                    for selected in selected_movies:
                        sim_movie = reverse_dict[selected]
                        genres_sim = get_set_overlap(movie_dict[sim_movie]['genres'], movie_dict[movie]['genres'])
                        sim_cast = [member['name'] for member in movie_dict[sim_movie]['cast']]
                        sim_crew = [member['name'] for member in movie_dict[sim_movie]['crew']]
                        cast = [member['name'] for member in movie_dict[movie]['cast']]
                        crew = [member['name'] for member in movie_dict[movie]['crew']]
                        crew_sim = get_set_overlap(sim_cast + sim_crew, cast + crew)
                        keywords_sim = get_set_overlap(movie_dict[sim_movie]['keywords'], movie_dict[movie]['keywords'])
                        cumulative_score += (genres_sim + crew_sim + keywords_sim) / (3 * len(selected_movies))
                    score_dict[movie] += cumulative_score * similar_score

        ########### FILTERING OF DICTIONARIES ###########
        # updates dicts with hard filters
        # for duration and release, also computes scores
        if duration:
            movie_dict, score_dict = user_duration.main(movie_dict,score_dict,duration,duration_score,0)
        if release_start or release_end:
            movie_dict, score_dict = user_release.main(movie_dict,score_dict,[release_start, release_end], release_score, 0)
        if ratings:
            movie_dict, score_dict = user_filters.filter_ratings(movie_dict, score_dict, selected_ratings, ratings_score)
        if languages:
            movie_dict, score_dict = user_filters.filter_languages(movie_dict, score_dict, selected_languages, languages_score)

        ########### CONSTRUCTION OF SCORE DICTIONARY ###########
        for movie in score_dict:
            if genres:
                jaccard_sim = get_set_overlap(selected_genres, movie_dict[movie]['genres'])
                score_dict[movie] += jaccard_sim * genres_score

            if castCrew:
                cast = [member['name'] for member in movie_dict[movie]['cast']]
                crew = [member['name'] for member in movie_dict[movie]['crew']]
                jaccard_sim = get_set_overlap(selected_crew, cast + crew)
                score_dict[movie] += jaccard_sim * castCrew_score

            if keywords:
                jaccard_sim = get_set_overlap(selected_keywords, movie_dict[movie]['keywords'])
                score_dict[movie] += jaccard_sim * keywords_score

            if acclaim == "yes":
                tmdb_score = movie_dict[movie]['tmdb_score_value']
                if tmdb_score >= 7.0:
                    score_dict[movie] += tmdb_score / 10.0 * acclaim_score
                else:
                    score_dict[movie] += tmdb_score / 20.0 * acclaim_score

            if popularity == "yes":
                tmdb_count = movie_dict[movie]['tmdb_score_count']
                if tmdb_count == 0:
                    tmdb_average = 0
                else:
                    tmdb_average = math.log(tmdb_count) / math.log(max_tmdb_count)
                imdb_count = movie_dict[movie]['imdb_score_count']
                if imdb_count == 0:
                    imdb_average = 0
                else:
                    imdb_average = math.log(imdb_count) / math.log(max_imdb_count)
                meta_count = movie_dict[movie]['meta_score_count']
                if meta_count == 0:
                    meta_average = 0
                else:
                    meta_average = math.log(meta_count) / math.log(max_meta_count)
                average_score = (tmdb_average + imdb_average + meta_average) / 3.0
                score_dict[movie] += average_score * popularity_score


        ########### SORT SCORES, RETURN TOP MATCHES ###########
        sorted_score_dict = sorted(score_dict.iteritems(), key=lambda (k,v): (v,k), reverse=True)[:24]

        if max_score == 0:
            for movie_tuple in sorted_score_dict:
                movie_id, movie_score = movie_tuple
                movie_dict[movie_id]['similarity'] = 0.0
                dt = datetime.datetime.strptime(movie_dict[movie_id]['release_date'], '%Y-%m-%d').strftime('%m-%d-%Y')
                movie_dict[movie_id]['release_date'] = dt
                data.append(movie_dict[movie_id])
        else:
            for movie_tuple in sorted_score_dict:
                movie_id, movie_score = movie_tuple
                movie_dict[movie_id]['similarity'] = movie_score / max_score * 100.0
                dt = datetime.datetime.strptime(movie_dict[movie_id]['release_date'], '%Y-%m-%d').strftime('%m-%d-%Y')
                movie_dict[movie_id]['release_date'] = dt
                data.append(movie_dict[movie_id])

        data = [data[i:i + 6] for i in xrange(0, len(data), 6)]

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
        data=data[:10],
        movie_list=movie_list,
        genre_list=genre_list,
        castCrew_list=castCrew_list,
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