from . import *


def weight(jac_res, cos_res):
    results = {}
    jacky = set(jac_res.keys())  # haha get it? jac_key -> jacky
    cos_key = set(cos_res.keys())
    both = jacky.intersection(cos_key)
    cos_only = cos_key.difference(jacky)
    jac_only = jacky.difference(cos_key)
    for key in both:
        results[key] = jac_res[key][0], jac_res[key][1] * \
            0.5 + cos_res[key][1]*0.5
    for key in cos_only:
        results[key] = cos_res[key][0], cos_res[key][1] * 0.5
    for key in jac_only:
        results[key] = jac_res[key][0], jac_res[key][1] * 0.5
    return results


def adj_minscore(min_score, results):
    final = []
    for joke in results:
        if results[joke][0]['score'] == 'None':
            final.append(
                (results[joke][0], "Similarity: " + str(results[joke][1]*0.67)))
        else:
            score_num = float(results[joke][0]['score'])
            if score_num >= min_score:
                final.append((results[joke][0], "Similarity: " +
                              str(results[joke][1]*0.67 + (0.33/5*score_num))))
            else:
                final.append((results[joke][0], "Similarity: " +
                              str(results[joke][1]*0.67 + (0.16/5*score_num))))
    jokes = Joke.query.filter( Joke.score >= min_score). all()
    blahblah = [
        ({"text": joke.text, "categories": joke.categories, "score": str(joke.score), "maturity": joke.maturity}, "Similarity: " + str(0.16/5*float(joke.score))) for joke in jokes
    ]
    final += blahblah  # used if no jac or cos joke outputs but min_score is provided
    return final
