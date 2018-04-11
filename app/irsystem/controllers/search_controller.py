from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "CinemaPop"
net_ids = "Angela Zhang: az337, Chris Fifty: cjf92, Newton Ni: cn279, Erik Chan: ejc233, Xinyu Zhao: xz293"

@irsystem.route('/', methods=['GET'])
def search():
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
		rec1 = dict()
		rec1['title'] = 'Avengers: Infinity War'
		rec1['similarity'] = 95.6
		rec1['poster'] = 'https://image.tmdb.org/t/p/w1280/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg'
		rec1['synopsis'] = 'As the Avengers and their allies have continued to protect the world from threats too large for any one hero to handle, a new danger has emerged from the cosmic shadows: Thanos. A despot of intergalactic infamy, his goal is to collect all six Infinity Stones, artifacts of unimaginable power, and use them to inflict his twisted will on all of reality. Everything the Avengers have fought for has led up to this moment - the fate of Earth and existence itself has never been more uncertain.'
		rec1['genres'] = 'Adventure, Action, Fantasy, Science Fiction'
		rec1['duration'] = '156'
		rec1['release'] = '04-07-2018'
		rec1['user_score'] = '123.45'
		rec1['cast'] = 'Robert Downey Jr., Chris Hemsworth, Mark Ruffalo'
		rec1['homepage'] = 'http://marvel.com/movies/movie/223/avengers_infinity_war_part_1'
		rec2 = dict()
		rec2['title'] = 'La La Land'
		rec2['similarity'] = 87.2
		rec2['poster'] = 'https://image.tmdb.org/t/p/w1280/ylXCdC106IKiarftHkcacasaAcb.jpg'
		rec2['synopsis'] = 'Mia, an aspiring actress, serves lattes to movie stars in between auditions and Sebastian, a jazz musician, scrapes by playing cocktail party gigs in dingy bars, but as success mounts they are faced with decisions that begin to fray the fragile fabric of their love affair, and the dreams they worked so hard to maintain in each other threaten to rip them apart.'
		rec2['genres'] = 'Comedy, Drama, Romance'
		rec2['duration'] = '128'
		rec2['release'] = '12-16-2016'
		rec2['user_score'] = '79.0'
		rec2['cast'] = 'Ryan Gosling, Emma Stone, John Legend'
		rec2['homepage'] = 'http://www.lalaland.movie/'
		rec3 = dict()
		rec3['title'] = 'Coco'
		rec3['similarity'] = 75.6
		rec3['poster'] = 'https://image.tmdb.org/t/p/w1280/eKi8dIrr8voobbaGzDpe8w0PVbC.jpg'
		rec3['synopsis'] = 'Despite his family\'s baffling generations-old ban on music, Miguel dreams of becoming an accomplished musician like his idol, Ernesto de la Cruz. Desperate to prove his talent, Miguel finds himself in the stunning and colorful Land of the Dead following a mysterious chain of events. Along the way, he meets charming trickster Hector, and together, they set off on an extraordinary journey to unlock the real story behind Miguel\'s family history.'
		rec3['genres'] = 'Adventure, Animation, Comedy, Family'
		rec3['duration'] = '105'
		rec3['release'] = '11-22-2017'
		rec3['user_score'] = '78.0'
		rec3['cast'] = 'Anthony Gonzalez, Gael Garcia Bernal, Benjamin Bratt'
		rec3['homepage'] = 'https://www.pixar.com/feature-films/coco'
		data = [rec1, rec2, rec3]
	return render_template('search.html', name=project_name, netids=net_ids, output_message=output_message, data=data)

