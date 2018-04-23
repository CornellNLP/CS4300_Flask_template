import numpy as np
import scipy.stats


# use the attribues of the similar movies to boost the parameters of our "query movie"
def boost_query(query_dict,sim_movies,movie_dict):
	selected_movies = set(sim_movies)
	for movie in movie_dict:
		if movie_dict[movie]['title'].lower() in selected_movies:
			query_dict['genres'] |= movie_dict[movie]['genres']
			query_dict['castCrew'] |= (movie_dict[movie]['cast'] + movie_dict[movie]['crew'])
	return query_dict

# vectorize the movies in terms of the query
def vectorize_movies(query_dict,movie_dict):
	mod_movie_dict = {}
	mod_movie_lst = []
	movie_lookup = []

	duration_score = gaussian_score_duration(movie_dict,query_dict['duration'],1,0)
	release_score = gaussian_score_release(movie_dict,query_dict['release_date'],1,0)

	for movie in movie_dict:
		tmp = []

		# list of genres for movie m -> jaccard sim with query
		mod_movie_dict[movie]['genres'] = get_set_overlap(query_dic['genres'],movie_dict[movie]['genres'])
		tmp.append(get_set_overlap(query_dic['genres'],movie_dict[movie]['genres']))

		# list of cast and crew for movie m -> jaccard sim with the query
		cast = [member['name'] for member in movie_dict[movie]['cast']]
        crew = [member['name'] for member in movie_dict[movie]['crew']]
        mod_movie_dict[movie]['castCrew'] = get_set_overlap(selected_crew, cast + crew)
        tmp.append(get_set_overlap(selected_crew, cast + crew))

        # keywords from query -> jaccard sim with the movie m synopsis
        mod_movie_dict[movie]['keywords'] = get_set_overlap(selected_keywords, movie_dict[movie]['keywords'])
        tmp.append(get_set_overlap(selected_keywords, movie_dict[movie]['keywords']))

        # duration & release date from movie m -> probabilistic gaussian fit around the mean 
        mod_movie_dict[movie]['duration'] = duration_score[movie]
        tmp.append(duration_score[movie])

        mod_movie_dict[movie]['release_date'] = duration_score[movie]
        tmp.append(duration_score[movie])

        mod_movie_lst.append(tmp)
        movie_lookup.append(movie)
        mod_movie_mat, movie_lookup = np.array(mod_movie_lst), np.array(movie_lookup)
        return mod_movie_dict, mod_movie_mat 

def knn_algo(mod_movie_mat,movie_lookup):
	n,d = mod_movie_mat.shape
	query = np.ones(d)
	dists = np.linalg.norm(Mod_movie_mat - query,axis=1,ord=2)
	top_ten = np.argsort(dists)[:10]
	return movie_lookup[top_ten]


########### HELPER FUNCTIONS ###########
def gaussian_score_duration(movie_dict,mean,high_val,low_val):
	score_dict = {}
	for movie in movie_dict:
		if movie_dict[movie]['runtime'] is None:
			movie_dict[movie]['runtime'] = 0

	dist = scipy.stats.norm(mean,10)
	movie_to_weight = {k:dist.pdf(v['runtime']) for k,v in movie_dict.iteritems()}
	max_val,min_val = max(movie_to_weight.values()), min(movie_to_weight.values())
	movie_to_weight = {k:((v - min_val)/(max_val - min_val)) for k,v in movie_to_weight.iteritems()}

	for movie in movie_dict:
		score_dict[movie] = movie_to_weight[movie]*(high_val + low_val) - low_val

	return score_dict

# get the fraction of items in list1 available in list2
def get_set_overlap(list1, list2):
    set1 = set([x.lower() for x in list1])
    set2 = set([x.lower() for x in list2])
    num = float(len(set1.intersection(set2)))
    den = len(set1)
    return num / den

