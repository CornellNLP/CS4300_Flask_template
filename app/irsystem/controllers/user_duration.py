import scipy.stats

def parse(inp):
	if "-" in inp:
		s = inp.split("-")
		lst = [int(entry.strip()) for entry in s]
		return lst
	return [int(inp.strip())]

def filter_hard(movie_dict,score_dict,low_bound, high_bound, high_val):
	rtn_movie = {}
	rtn_score = {}
	for movie in movie_dict:
		if movie_dict[movie]['runtime'] >= low_bound and movie_dict[movie]['runtime'] <= high_bound:
			rtn_movie[movie] = movie_dict[movie]
			rtn_score[movie] = score_dict[movie] + high_val
	return rtn_movie,rtn_score

# gaussian weighted appropriately: update the score_dict
def gaussian_score(movie_dict,score_dict,mean,high_val,low_val):

	# if the movie runtime is a nonetype....
	for movie in movie_dict:
		if movie_dict[movie]['runtime'] is None:
			movie_dict[movie]['runtime'] = 0

	dist = scipy.stats.norm(mean,10)
	movie_to_weight = {k:dist.pdf(v['runtime']) for k,v in movie_dict.iteritems()}
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
		return filter_hard(movie_dict,score_dict,vals[0],vals[1], high_val)
	return movie_dict,gaussian_score(movie_dict,score_dict,vals[0],high_val,low_val)
