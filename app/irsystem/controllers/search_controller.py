from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import json
import gaussian
from random import *

project_name = "CinemaPop"
net_ids = "Angela Zhang: az337, Chris Fifty: cjf92, Newton Ni: cn279, Erik Chan: ejc233, Xinyu Zhao: xz293"

year_lst = []
for x in range(1900,2019):
	year_lst.append(x)

@irsystem.route('/', methods=['GET'])
def search():
	output_message = ""
	data = []
	movies_json = json.load(open('movies.json'))
	genres_json = json.load(open('genres.json'))
	movie_list = [movie['title'] for movie in movies_json]
	genre_list = [genre['name'] for genre in genres_json['genres']]

	similar = request.args.get('similar')
	genres = request.args.get('genres')
	duration = request.args.get('duration')
	release = request.args.get('release')
	acclaim = request.args.get('acclaim')
	castCrew = request.args.get('castCrew')
	keywords = request.args.get('keywords')
	year_range = [request.args.get('year_start'), request.args.get('year_end')]
	query = [similar, genres, duration, release, acclaim, castCrew, keywords]
	if not query[0] and not query[1] and not query[2] and not query[3] and not query[4] and not query[5] and not query[6]:
		data = []
		output_message = ''
	else:
		selected_movies = []
		if similar:
			names = []
			if ';' in similar:
				names = similar.split(";")
			for n in names:
				selected_movies.append(n.lower());
				
		data = []
		movie_dict = dict()
		score_dict = dict()

		for movie in movies_json:
			movie_dict[movie['id']] = movie
			score_dict[movie['id']] = 0.0


		# modify movie_dict and score_dict to account for the "duration" user input 
		# assuming duration is in the form "90-180" rather than "180 - 90"
		movie_dict,score_dict = gaussian.main(movie_dict,score_dict,duration,10,0)



		for movie in score_dict:


			#if duration and movie_dict[movie]['runtime'] == int(duration):
				#score_dict[movie] += 10.0

			if genres and genres in set(movie_dict[movie]['genres']):
				score_dict[movie] += 20.0
			if acclaim == "yes":
				if movie_dict[movie]['vote_average'] > 7.0:
					score_dict[movie] += movie_dict[movie]['vote_average'] + 10.0
				if movie_dict[movie]['vote_average'] < 7.0:
					score_dict[movie] -= 100.0

		sorted_score_dict = sorted(score_dict.iteritems(), key=lambda (k,v): (v,k), reverse=True)[:20]

		for movie_tuple in sorted_score_dict:
			movie_id, movie_score = movie_tuple
			movie_dict[movie_id]['similarity'] = movie_score
			movie_dict[movie_id]['poster'] = 'https://image.tmdb.org/t/p/w1280/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg'
			data.append(movie_dict[movie_id])

		output_message = "Your search has been processed."
			# rec0 = movies_json[randint(0, len(movie_list) - 1)]
			# rec0['similarity'] = 95.6
			# rec0['poster'] = 'https://image.tmdb.org/t/p/w1280/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg'
			# rec1 = movies_json[randint(0, len(movie_list) - 1)]
			# rec1['similarity'] = 87.2
			# rec1['poster'] = 'https://image.tmdb.org/t/p/w1280/ylXCdC106IKiarftHkcacasaAcb.jpg'
			# rec2 = movies_json[randint(0, len(movie_list) - 1)]
			# rec2['similarity'] = 75.6
			# rec2['poster'] = 'https://image.tmdb.org/t/p/w1280/eKi8dIrr8voobbaGzDpe8w0PVbC.jpg'

			# data = [rec0, rec1, rec2]
	return render_template('search.html', name=project_name, netids=net_ids, output_message=output_message, data=data, movie_list=movie_list, genre_list=genre_list, year_list= year_lst)
