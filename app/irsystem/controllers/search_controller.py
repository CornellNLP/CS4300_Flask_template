from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import json
import user_duration
import user_release
from random import *

movies_json = json.load(open('app/static/data/movies.json'))
genres_json = json.load(open('genres.json'))
movie_list = [movie['title'] for movie in movies_json]
genre_list = [genre['name'] for genre in genres_json['genres']]
year_lst = range(1900, 2019)

@irsystem.route('/', methods=['GET'])
def search():
    output_message = ""
    data = []

    # user inputs
    similar = request.args.get('similar')
    genres = request.args.get('genres')
    release = request.args.get('release')
    acclaim = request.args.get('acclaim')
    castCrew = request.args.get('castCrew')
    keywords = request.args.get('keywords')
    duration = request.args.get('duration')

    if not similar and not genres and not duration and not release and not acclaim and not castCrew and not keywords:
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

        selected_movies = parse_lst_str(similar)
        selected_genres = parse_lst_str(genres)
        print castCrew
        selected_crew = parse_lst_str(castCrew)
        print selected_crew
        selected_keywords = parse_lst_str(keywords)

        if similar:
            similar_score = 10.0
            max_score += similar_score
        if genres:
            genres_score = 10.0
            max_score += genres_score
        if release:
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
        if release:
            movie_dict, score_dict = user_release.main(movie_dict,score_dict,release,4,0)
        if duration:
            movie_dict, score_dict = user_duration.main(movie_dict,score_dict,duration,10,0)

        for movie in score_dict:
            if similar:
                x = "hi"
            if genres:
                jaccard_sim = get_set_overlap(selected_genres, movie_dict[movie]['genres'])
                score_dict[movie] += jaccard_sim * genres_score
            if acclaim == "yes":
                tmdb_score = movie_dict[movie]['tmdb_score_value']
                if tmdb_score >= 7.0:
                    score_dict[movie] += tmdb_score / 10.0 * acclaim_score
                else:
                    score_dict[movie] -= 100.0
            if castCrew:
                cast = [member['name'] for member in movie_dict[movie]['cast']]
                crew = [member['name'] for member in movie_dict[movie]['crew']]
                jaccard_sim = get_set_overlap(selected_crew, cast + crew)
                score_dict[movie] += jaccard_sim * castCrew_score
            if keywords:
                jaccard_sim = get_set_overlap(selected_keywords, movie_dict[movie]['keywords'])
                score_dict[movie] += jaccard_sim * keywords_score

        sorted_score_dict = sorted(score_dict.iteritems(), key=lambda (k,v): (v,k), reverse=True)[:20]

        for movie_tuple in sorted_score_dict:
            movie_id, movie_score = movie_tuple
            movie_dict[movie_id]['similarity'] = movie_score / max_score * 100.0
            data.append(movie_dict[movie_id])

        output_message = "Your search has been processed."

    return render_template('search.html', output_message=output_message, data=data, movie_list=movie_list, genre_list=genre_list, year_list= year_lst)

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
