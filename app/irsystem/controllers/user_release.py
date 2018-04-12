import scipy.stats

def parse(inp):
	if "-" in inp:
		s = inp.split("-")
		lst = [int(entry[:4].strip()) for entry in s]
		return lst
	return [int(inp[:4].strip())]

def filter_hard(movie_dict,score_dict,low_bound, high_bound):
	rtn_movie = {}
	rtn_score = {}
	for movie in movie_dict:
		if int(movie_dict[movie]['release_date'][:4]) >= low_bound and int(movie_dict[movie]['release_date'][:4]) <= high_bound:
			rtn_movie[movie] = movie_dict[movie]
			rtn_score[movie] = score_dict[movie]
	return rtn_movie,rtn_score

# gaussian weighted appropriately: update the score_dict
def gaussian_score(movie_dict,score_dict,mean,high_val,low_val):

	mod_movie_dict = dict(movie_dict)

	# if the movie runtime is a nonetype....
	for movie in mod_movie_dict:
		if mod_movie_dict[movie]['release_date'] is None:
			mod_movie_dict[movie]['release_date'] = int("0000")
		else:
			mod_movie_dict[movie]['release_date'] = int(mod_movie_dict[movie]['release_date'][:4])

	dist = scipy.stats.norm(mean,4)
	movie_to_weight = {k:dist.pdf(v['release_date']) for k,v in mod_movie_dict.iteritems()}
	max_val,min_val = max(movie_to_weight.values()), min(movie_to_weight.values())

	# movie -> weight value between 0 and 1
	movie_to_weight = {k:((v - min_val)/(max_val - min_val)) for k,v in movie_to_weight.iteritems()}

	# movie -> weight value between high and low
	for movie in score_dict:
		score_dict[movie] = score_dict[movie] + (movie_to_weight[movie]*(high_val + low_val) - low_val)
	return score_dict

def main(movie_dict,score_dict, inp, high_val,low_val):
	vals = parse(inp)
	if len(vals) == 2:
		return filter_hard(movie_dict,score_dict,vals[0],vals[1])
	return movie_dict,gaussian_score(movie_dict,score_dict,vals[0],high_val,low_val)
