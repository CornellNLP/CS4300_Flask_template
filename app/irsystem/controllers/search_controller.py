from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import json
import user_duration
import user_release
from random import *

movies_json = json.load(open('app/static/data/movies.json'))
movie_dict = dict()
for movie in movies_json:
    movie_dict[movie['id']] = json.load(open('app/static/data/movies/' + movie['id'] + '.json'))
genres_json = json.load(open('genres.json'))
movie_list = [movie['title'] for movie in movies_json]
genre_list = [genre['name'] for genre in genres_json['genres']]
castCrew_list = []
keywords_list = []
for movie in movie_dict:
    castCrew_list += ([member['name'] for member in movie_dict[movie]['cast']] + [member['name'] for member in movie_dict[movie]['crew']])
    keywords_list += movie_dict[movie]['keywords']
castCrew_list = list(set(castCrew_list))
keywords_list = list(set(keywords_list))
year_list = range(1900, 2019)

@irsystem.route('/', methods=['GET'])
def search():
    output_message = ""
    data = []

    # user inputs
    similar = request.args.get('similar')
    genres = request.args.get('genres')
    acclaim = request.args.get('acclaim')
    castCrew = request.args.get('castCrew')
    keywords = request.args.get('keywords')
    duration = request.args.get('duration')
    release_start = request.args.get('release_start')
    release_end = request.args.get('release_end')

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

        selected_movies = parse_lst_str(similar)
        selected_genres = parse_lst_str(genres)
        selected_crew = parse_lst_str(castCrew)
        selected_keywords = parse_lst_str(keywords)

        if similar:
            similar_score = 10.0
            max_score += similar_score
        if genres:
            genres_score = 10.0
            max_score += genres_score
        if release_start and release_end:
            release_score = 10.0
            max_score += release_score
        if acclaim == "yes":
            acclaim_score = 10.0
            max_score += acclaim_score
        if castCrew:
            castCrew_score = 10.0
            max_score += castCrew_score
        if keywords:
            keywords_score = 10.0
            max_score += keywords_score
        if duration:
            duration_score = 10.0
            max_score += duration_score

        # modify movie_dict and score_dict to account for the "duration" user input
        # assuming duration is in the form "90-180" rather than "180 - 90"
        if duration:
            movie_dict, score_dict = user_duration.main(movie_dict,score_dict,duration,duration_score,0)
        if release_start and release_end:
            movie_dict, score_dict = user_release.main(movie_dict,score_dict,[release_start, release_end], release_score, 0)

        for movie in score_dict:
            if similar:
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


            if genres:
                jaccard_sim = get_set_overlap(selected_genres, movie_dict[movie]['genres'])
                score_dict[movie] += jaccard_sim * genres_score
            if acclaim == "yes":
                tmdb_score = movie_dict[movie]['tmdb_score_value']
                if tmdb_score >= 7.0:
                    score_dict[movie] += tmdb_score / 10.0 * acclaim_score
                else:
                    score_dict[movie] += tmdb_score / 20.0 * acclaim_score
            if castCrew:
                cast = [member['name'] for member in movie_dict[movie]['cast']]
                crew = [member['name'] for member in movie_dict[movie]['crew']]
                jaccard_sim = get_set_overlap(selected_crew, cast + crew)
                score_dict[movie] += jaccard_sim * castCrew_score
            if keywords:
                jaccard_sim = get_set_overlap(selected_keywords, movie_dict[movie]['keywords'])
                score_dict[movie] += jaccard_sim * keywords_score

        sorted_score_dict = sorted(score_dict.iteritems(), key=lambda (k,v): (v,k), reverse=True)[:20]

        if max_score == 0:
            for movie_tuple in sorted_score_dict:
                movie_id, movie_score = movie_tuple
                movie_dict[movie_id]['similarity'] = 0.0
                data.append(movie_dict[movie_id])
        else:
            for movie_tuple in sorted_score_dict:
                movie_id, movie_score = movie_tuple
                movie_dict[movie_id]['similarity'] = movie_score / max_score * 100.0
                data.append(movie_dict[movie_id])

        data = [data[i:i + 5] for i in xrange(0, len(data), 5)]
        output_message = "Your search has been processed."

    return render_template('search.html', output_message=output_message, data=data, movie_list=movie_list, genre_list=genre_list, castCrew_list= castCrew_list, keywords_list = keywords_list, year_list = year_list)

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
