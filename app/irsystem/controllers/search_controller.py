from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import json
from random import *

project_name = "CinemaPop"
net_ids = "Angela Zhang: az337, Chris Fifty: cjf92, Newton Ni: cn279, Erik Chan: ejc233, Xinyu Zhao: xz293"

@irsystem.route('/', methods=['GET'])
def search():
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
	query = [similar, genres, duration, release, acclaim, castCrew, keywords]
	if not query[0] and not query[1] and not query[2] and not query[3] and not query[4] and not query[5] and not query[6]:
		data = []
		output_message = ''
	else:

		output_message = "Your search has been processed."
		rec0 = movies_json[randint(0, len(movie_list) - 1)]
		rec0['similarity'] = 95.6
		rec0['poster'] = 'https://image.tmdb.org/t/p/w1280/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg'
		rec1 = movies_json[randint(0, len(movie_list) - 1)]
		rec1['similarity'] = 87.2
		rec1['poster'] = 'https://image.tmdb.org/t/p/w1280/ylXCdC106IKiarftHkcacasaAcb.jpg'
		rec2 = movies_json[randint(0, len(movie_list) - 1)]
		rec2['similarity'] = 75.6
		rec2['poster'] = 'https://image.tmdb.org/t/p/w1280/eKi8dIrr8voobbaGzDpe8w0PVbC.jpg'

		data = [rec0, rec1, rec2]
	return render_template('search.html', name=project_name, netids=net_ids, output_message=output_message, data=data, movie_list=movie_list, genre_list=genre_list)

