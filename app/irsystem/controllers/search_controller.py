from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from .json_reader import *
from .cosine_similarity import *
from .personality_vector import *

project_name = "Perfect Wine Match: Find Your Perfect Wine"
net_id = "Ashley Park: ap764, Junho Kim-Lee: jk2333, Sofia Yoon: hy348, Yubin Heo: yh356"

df = json_read("app/irsystem/controllers/winemag_data_withtoks.json")
df_personality = json_read("app/irsystem/controllers/wine_personality.json")

inv_ind, idf, norms = precompute(df["toks"])
legend, index, mat = json_read_vector(
    "app/irsystem/controllers/wine_variety_vectors.json")

# Personality data
tokenized_personality = tokenizer_personality_data(df_personality)
tokenized_variety = tokenizer_personality_variety(df_personality)
flat_tokenized_variety = flat_tokenizer_personality_variety(df_personality)
inv_ind_person, idf_person, norms_person = precompute_personality(
    tokenized_personality)

# @irsystem.route('/', methods=['GET'])
# def search():
# 	query = request.args.get('search')
# 	if not query:
# 		data = []
# 		output_message = ''
# 	else:
# 		cosine = cossim(query, inv_ind, idf, norms)
# 		data = compute_outputs(query, cosine, df, 10)
# 		output_message = "Your search: " + query
# 		# data = range(5)
# 	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)


@irsystem.route('/', methods=['GET'])
def search():
    name = request.args.get('name')
    p1 = request.args.get('personality1')
    p2 = request.args.get('personality2')
    p3 = request.args.get('personality3')
    p4 = request.args.get('personality4')
    p5 = request.args.get('personality5')
    p6 = request.args.get('personality6')
    p7 = request.args.get('personality7')
    p8 = request.args.get('personality8')
    scale = [0, 1, 2, 3, 4, 5]
    flavor = request.args.get('flavor')
    scent = request.args.get('scent')
    price = request.args.get('price')
    print(price)

    if not p1 or not p2 or not p3 or not p4 or not p5 or not p6 or not p7 or not p8:
        personality_match = ''
        wine_match = ''
    else:
        responses = [
            int(p1),
            int(p2),
            int(p3),
            int(p4),
            int(p5),
            int(p6),
            int(p7),
            int(p8)
        ]
        wine_scores = compute_personality_vec(legend, index, mat, responses)
        flavor_result = cossim_dict(flavor, inv_ind, idf, norms)
        scent_result = cossim_dict(scent, inv_ind, idf, norms)
        total = total_score(flavor_result, scent_result)

        personality_match = compute_personality(name, wine_scores,
                                                df_personality)
        wine_match = compute_wine(name, wine_scores, total, df, 5, price)

    return render_template('search.html',
                           name=project_name,
                           user_name=name,
                           netid=net_id,
                           scale=scale,
                           personality_match=personality_match,
                           wine_match=wine_match)
