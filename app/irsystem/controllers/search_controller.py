from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from .json_reader import json_read
from .cosine_similarity import *

project_name = "Wine Time: Your Personal Sommelier"
net_id = "Ashley Park: ap764, Junho Kim-Lee: jk2333, Sofia Yoon: hy348, Yubin Heo: yh356"

df = json_read("app/irsystem/controllers/winemag_data_withtoks.json")
df_personality = json_read("app/irsystem/controllers/wine_personality.json")

inv_ind, idf, norms = precompute(df["toks"])

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
	flavor = request.args.get('flavor')
	scent = request.args.get('scent')
	personality1 = request.args.get('personality1')
	personality2 = request.args.get('personality2')
	personality3 = request.args.get('personality3')
	personality4 = request.args.get('personality4')
	personality5 = request.args.get('personality5')
	personality6 = request.args.get('personality6')
	adjectives = [
        'laid-back', 'adaptable', 'easygoing', 'empathetic', 'responsible',
        'helper-at-heart', 'facilitator', 'sophisticated', 'alpha', 'sexy',
        'powerful', 'put-together', 'social', 'adventurous', 'outgoing',
        'exuberant', 'accepting', 'outgoing', 'friendly', 'exuberant', 'fun',
        'spontaneous', 'genuine', 'loving', 'emotional', 'mysterious',
        'tolerant', 'pragmatic', 'flirty', 'sweet', 'sarcastic', 'authentic',
        'kind', 'genuine', 'good', 'nice', 'passionate', 'stylish', 'bold',
        'confident', 'classy', 'proud', 'refined', 'detail-oriented',
        'independent', 'driven', 'charming', 'attractive', 'socialite',
        'gullible', 'hard worker', 'smart', 'quiet', 'critical', 'analytical',
        'elegant', 'fresh', 'graceful', 'focused', 'skeptical', 'thinker',
        'young', 'happy', 'dreamer', 'resourceful', 'outspoken', 'realistic',
        'decisive', 'organized', 'conservative', 'serious', 'traditional',
        'systematic', 'leader', 'friendly', 'loyal', 'conscientious',
        'visionary', 'loyal', 'understander', 'idealistic', 'sensitive',
        'goal-oriented', 'tolerant'
    ]
	if not name or not flavor or not scent or not personality1:
		if not personality2 or not personality3 or not personality4:
			if not personality5 or not personality6:
				data = []
				personality_data = []
				output_message = ''
	else:
		personality = personality1 + ' ' + personality2 + ' ' + personality3
		personality += ' ' + personality4 + ' ' + personality5 + ' ' + personality6
		flavor_result = cossim_dict(flavor, inv_ind, idf, norms)
		scent_result = cossim_dict(scent, inv_ind, idf, norms)
		personality_result = cossim_dict(personality, inv_ind_person,
											idf_person, norms_person)
		personality_only_data = cossim(personality, inv_ind_person, idf_person, norms_person)
		total = total_score(flavor_result, scent_result, personality_result,
								df, tokenized_variety, flat_tokenized_variety)
		data = compute_outputs(name, total, df, 10)
		personality_data = compute_outputs_personality(personality_only_data, df_personality)
		output_message = "Matches for " + name
        # data = range(5)
	return render_template('search.html',
                           name=project_name,
                           netid=net_id,
                           output_message=output_message,
                           adjectives=adjectives,
                           data=data,
						   personality_only = personality_data)
