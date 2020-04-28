from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from flask import request, jsonify
from sqlalchemy import and_, or_, func
from itertools import combinations
import re
import math
from collections import Counter

from app import db
from app.irsystem.models import (
    Recipe, 
    Category,
    RecipeCategorization,
    RecipeSchema
)

recipe_schema = RecipeSchema(many=True)

"""
full_data = None
with open("app/full_format_recipes.json") as f:
    full_data = json.loads(f.readlines()[0])
"""

def tokenize(text):
    """Returns a list of words that make up the text.
        
    We lowercase everything.
    Regex is used to satisfy this function
        
    Params: {text: String}
    Returns: List
    """
    return re.findall('[a-z]+',text.lower())


def build_inverted_index(rcps,field):
    """ Builds an inverted index from the recipe field.
    Field can be "title", "desc", "categories", "ingredients", or
    "directions", "meal_type".
    Arguments
    =========
    rcps: list of dicts.
    field: a key in the dicts.
    Returns
    =======
    inverted_index: dict
        For each term, the index contains 
        a sorted list of tuples (doc_id, count_of_term_in_doc)
        such that tuples with smaller doc_ids appear first:
        inverted_index[term] = [(d1, tf1), (d2, tf2), ...]
    """
    bofw = set()
    # handling set case of meal_type
    if field == "meal_type":
        bofw = {"breakfast", "lunch", "dinner"}
    else:
        for rec in rcps:
            if rec:
                if rec[field] is not None:
                    words = tokenize(rec[field])
                    for w in words:
                        bofw.add(w)
    
    # initialize inverted index
    inverted_index = dict.fromkeys(bofw,list())
    for k, _ in inverted_index.items():
        inverted_index[k] = list()

    # build inverted index
    for d_id, recipe in enumerate(rcps):
        if recipe[field] is not None:
            words = tokenize(recipe[field])
            for w in set(words):
                inverted_index[w].append((d_id, words.count(w)))
    return inverted_index


def combine_AND_boolean_terms(terms, inverted_index):
    """ Returns the recipe ids that contain 
        all the words in terms.
    """
    if len(terms) == 0:
        return []
    term_to_postings = {}
    for term in terms:
        if term in inverted_index:
            term_l = term.lower()
            term_to_postings[term_l] = [tup[0] for tup in inverted_index[term]]
    
    if len(term_to_postings) == 0:
        return []
    # most efficient run-time, order by number of postings ascending
    terms_in_order = [k for k in sorted(term_to_postings, key=lambda k: len(term_to_postings[k]), reverse=False)] 
    postings = term_to_postings[terms_in_order[0]]
    for i in range(1, len(terms_in_order)):
        postings = merge_postings_ANDAND(postings,term_to_postings[terms_in_order[i]])
    return postings


def combine_NOT_boolean_terms(terms_not,inverted_index):
    """ Returns the recipe ids that contain any of the words in terms.
    """
    if len(terms_not) == 0:
        return []
    term_to_postings = {}
    for term in terms_not:
        if term in inverted_index:
            term_l = term.lower()
            term_to_postings[term_l] = [tup[0] for tup in inverted_index[term]]
    
    if len(term_to_postings) == 0:
        return []
    # most efficient run-time, order by largest document id, ascending
    terms_in_order = [k for k in sorted(term_to_postings, key=lambda k: max(term_to_postings[k]), reverse=False) ]
    postings = term_to_postings[terms_in_order[0]]
    for i in range(1, len(terms_in_order)):
        postings = merge_postings_OROR(postings,term_to_postings[terms_in_order[i]])
    return postings


def merge_postings_ANDAND(postings1, postings2):
    """ Returns the documents in postings1 and postings2.
    """
    merged_postings = [p for p in postings1 if p in postings2]
    return merged_postings


def merge_postings_OROR(postings1, postings2):
    """ Returns the documents in postings1 or postings2.
    """
    merged_postings = postings1
    for p in postings2:
        if p not in merged_postings:
            merged_postings.append(p)
    return sorted(merged_postings)


def merge_postings_ANDNOT(postings1, postings2):
    """ Returns the documents in postings1 and not in postings2.
        
    """
    merged_postings = [p for p in postings1 if p not in postings2]
    return merged_postings


def rank_recipes_boolean(fav_foods,omit_foods,inv_idx,rcps):
    """ Returns the matching recipes in order of best rating

        Params: {fav_foods: List of str
                omit_foods: List of str
                inv_idx: List of tuples
                rcps: List of Dicts
                }

        Returns: recipes: List of Dicts
    """
    rec_ids = merge_postings_ANDNOT(combine_AND_boolean_terms(fav_foods,inv_idx), combine_NOT_boolean_terms(omit_foods,inv_idx))
    if len(rec_ids) == 0:
        return []
    recipes = [rcps[i] for i in rec_ids]
    for r in recipes:
        if r['rating'] is None or r['rating'] > 5:
            r['rating'] = 0
    recipes = sorted(recipes, key=lambda k: k['rating'], reverse=True)
    return recipes


def group_recipes(recipe_list,rsps,cal_lowbound,cal_upbound):
    """
    Returns a list of tuples (?) or lists (?) with three recipes in each
  
    Params: {recipe_list: a list of boolean matching sorted recipes
             cal_lowbound: an int
             cal_upbound: an int}
    Returns: List
    """
    recipe_groups = []
    if len(recipe_list) >= 3:
        for (r1, r2, r3) in combinations(recipe_list, 3):
            if len(recipe_groups) == 3:
                break
            if r1['calories'] is None or r2['calories'] is None or r3['calories'] is None:
                continue
            if (r1['calories'] + r2['calories'] + r3['calories'] >= cal_lowbound 
                and r1['calories'] + r2['calories'] + r3['calories'] <= cal_upbound):
                recipe_groups.append([r1, r2, r3])
    return recipe_groups


# cosine similarity
# min_freq and max_freq don't seem to work right: 
# min_freq excludes too many and max_freq excludes too few
def compute_idf(inv_idx, doc_num, min_freq, max_freq):
    """
    creates a dict of doc-idf pairs
    idf is calculated by:
    log(n / (1+df)), where n is number of documents and df is document frequency
    
    params: { inv_idx: an inverted index, type Dict
              doc_num: number of documents, type int
              min_freq: minimum frequency to appear in idf, type float
              max_freq: maximum frequency to appear in idf, type float
            }
    
    returns: dict
    """
    idf_dict = dict()
    for word in inv_idx.keys():
        df = len(inv_idx[word])

        #excludes too-common or not-common-enough terms
        if (df / doc_num) >= min_freq and (df / doc_num) <= max_freq:
            idf_dict[word] = math.log2(doc_num / (1 + df))
    return idf_dict


def compute_norms(idf_dict, inv_idx, doc_num):
    """
    returns a np array of document norms such that:
    array[i] = the norm of document i
    
    params: { idf_dict: a dictionary of doc-idf pairings, type Dict
              inv_idx: an inverted index, type Dict
              doc_num: number of documents, type int
            }
            
    returns: type np.array
    """
    norm_array = np.zeros(doc_num)
    
    #calculates sigma (tf*idf) ** 2
    for word in idf_dict.keys():
        for doc_id, tf in inv_idx[word]:
            norm_array[doc_id] += (tf * idf_dict[word]) ** 2
    return norm_array ** (1 / 2)


def cosine_sim(query_words, inv_idx, norms, idf_dict, recipes):
    """
    returns a list of results by cosine similarity
    performs a cosine search:
    cossim = (q*d) / (||q||*||d||)
    
    params: { query: the user's search query, type string
              inv_idx: an inverted index, type dict
              norms: document norms as calculated above, type dict
              idf_dict: term idf scores as calculated above, type dict
              recipes: list of all recipes being considered
            }
            
    returns: a list
    """
    # query vector and norm construction
    q_vector = {}
    q_norm = 0
    
    for word in query_words:
        q_vector[word] = query_words.count(word)
        q_norm += (q_vector[word] * (idf_dict[word] if word in idf_dict.keys() else 0)) ** 2
        
    q_norm = math.sqrt(q_norm)
    
    # intermediate dictionary used for calculating numerator (tf(q)*idf(q)*tf(d)*idf(d))
    # key is doc id, value is numerator
    inter_dict = {}
    
    # loops over words and documents
    for word in set(query_words):
        # filters out terms without idf scores
        if word in idf_dict.keys():
            for tup in inv_idx[word]:
                if tup[0] in inter_dict.keys():
                    inter_dict[tup[0]] += tup[1] * q_vector[word] * (idf_dict[word] ** 2)
                else:
                    inter_dict[tup[0]] = tup[1] * q_vector[word] * (idf_dict[word] ** 2)
    # divides by denominator and constructs results list
    results = []
    for doc in inter_dict.keys():
        num = inter_dict[doc]
        results.append((doc, num / q_norm*norms[doc]))
    
    results.sort(key=lambda t: t[1], reverse=True)
    recipe_ids = [id for id, _ in results[:10]]
    recipes = [recipes[i] for i in recipe_ids]
    return recipes


def query_split(query, inv_idx_meal_types, inv_idx_ingrds):
    """ Assumes query is at least three words.
        If a query word is not in the ingredients, returns None.
        
        Returns: list with length query
    """

    query_words = tokenize(query)

    qword_meal_counts = {} # query word : [# breakfast recipes, # lunch recipes, # dinner recipes]
        
    postings_brk = [tup[0] for tup in inv_idx_meal_types["breakfast"] ]
    postings_lun = [tup[0] for tup in inv_idx_meal_types["lunch"] ]
    postings_din = [tup[0] for tup in inv_idx_meal_types["dinner"] ]

    # compute probabilties
    for w in query_words:
        if w not in inv_idx_ingrds:
            return None
        postings_qword = [tup[0] for tup in inv_idx_ingrds[w] ]
        qword_meal_counts[w] = [ len( merge_postings_ANDAND(postings_qword, postings_brk) ) ,
                                len( merge_postings_ANDAND(postings_qword, postings_lun) ) ,
                                len( merge_postings_ANDAND(postings_qword, postings_din) ) ]
        tot = sum(qword_meal_counts[w])
        qword_meal_counts[w] = [count/tot for count in qword_meal_counts[w] ] # normalize by number recipes
    
    # get most probable meal type assignments to query words
    assignments = ["breakfast","lunch","dinner"]
    start_p = dict.fromkeys(assignments,1/len(assignments))
    trans_p = dict.fromkeys(assignments,start_p)
    emit_p = {}
    for a in assignments:
        emis = {}
        for w in query_words:
            emis[w] = qword_meal_counts[w][assignments.index(a)]
        tot = sum(emis.values())
        for k,v in emis.items():
            emis[k] = v/tot
        emit_p[a] = emis
    opt_assign = viterbi(query_words,assignments,start_p,trans_p,emit_p)
        
    # if there a meal type is excluded from the optimal assignment, coerce
    counts = Counter(opt_assign)
    if "breakfast" not in opt_assign:
        meal_most = max(counts, key=counts.get)
        opt_assign[opt_assign.index(meal_most)] = "breakfast"
    if "lunch" not in opt_assign:
        meal_most = max(counts, key=counts.get)
        opt_assign[opt_assign.index(meal_most)] = "lunch"
    if "dinner" not in opt_assign:
        meal_most = max(counts, key=counts.get)
        opt_assign[opt_assign.index(meal_most)] = "dinner"
    return opt_assign



def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    for st in states:
        V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}
    # Run Viterbi when t > 0
    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            max_tr_prob = V[t-1][states[0]]["prob"]*trans_p[states[0]][st]
            prev_st_selected = states[0]
            for prev_st in states[1:]:
                tr_prob = V[t-1][prev_st]["prob"]*trans_p[prev_st][st]
                if tr_prob > max_tr_prob:
                    max_tr_prob = tr_prob
                    prev_st_selected = prev_st
                    
            max_prob = max_tr_prob * emit_p[st][obs[t]]
            V[t][st] = {"prob": max_prob, "prev": prev_st_selected}
                    
    opt = []
    max_prob = 0.0
    previous = None
    # Get most probable state and its backtrack
    for st, data in V[-1].items():
        if data["prob"] > max_prob:
            max_prob = data["prob"]
            best_st = st
    opt.append(best_st)
    previous = best_st
    
    # Follow the backtrack till the first observation
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["prev"])
        previous = V[t + 1][previous]["prev"]
    
    return opt


def sort_recipes(recipes):
    breakfast = []
    lunch = []
    dinner = []
    for r in recipes:
        if r["meal_type"] == "breakfast":
            breakfast.append(r)
        elif r["meal_type"] == "lunch":
            lunch.append(r)
        else:
            dinner.append(r)
    return breakfast, lunch, dinner


project_name = "Fitness Dream Team"
net_ids = "Henri Clarke: hxc2, Alice Hu: ath84, Michael Pinelis: mdp93, Genghis Shyy: gs484, Sam Vacura: smv66"

def version_1_search(query, output_message, data):
    if query:
        query = query.lower()
        query_words = query.split(",")
        query_words = [word.strip() for word in query_words]
        if len(query_words) == 1:
            query_words = query_words[0].split(";")
        recipes = Recipe.query.filter(
            or_(
                or_(Recipe.title.like("%{}%".format(word)) for word in query_words),
                or_(Recipe.description.like("%{}%".format(word)) for word in query_words),
                or_(Recipe.ingredients.like("%{}%".format(word)) for word in query_words),
                or_(Recipe.directions.like("%{}%".format(word)) for word in query_words)
            )
        ).all()
        if not recipes:
            output_message = "No Results Found :("
            data = []
        else:
            recipes_out = recipe_schema.dump(recipes)
            inv_idx_ingredients = build_inverted_index(recipes_out, "ingredients")

            # hardcoding []; will replace after input for "foods to omit" is added
            ranked_results = rank_recipes_boolean(query_words, [], inv_idx_ingredients, recipes_out)
            if len(ranked_results) == 0:
                output_message = "No Results Found :(("
                data = []
            else:
                output_message = "Your search: " + query
                data = ranked_results[:10]
    return output_message, data


def version_2_search(query_words, omit_words, recipes):
    all_data = []
    if not recipes:
        all_data = []
        """
        # cosine similarity 
        recipes_out = recipe_schema.dump(Recipe.query.all())
        num_recipes = len(recipes_out)
        inv_idx_ingredients = build_inverted_index(recipes_out, "ingredients")
        idf_dict = compute_idf(inv_idx_ingredients, num_recipes, 0.1, 0.9)
        norms = compute_norms(idf_dict, inv_idx_ingredients, num_recipes)
        ranked_results = cosine_sim(query_words, inv_idx_ingredients, norms, idf_dict, recipes_out)
        if len(ranked_results) == 0:
            all_data = []
        else:
            all_data = ranked_results
        """
    else:
        # boolean search
        recipes_out = recipe_schema.dump(recipes)
        inv_idx_ingredients = build_inverted_index(recipes_out, "ingredients")
        inv_idx_title = build_inverted_index(recipes_out, "title")
        ranked_results = rank_recipes_boolean(query_words, omit_words, inv_idx_ingredients, recipes_out)
        if len(ranked_results) == 0:
            ranked_results = rank_recipes_boolean(query_words, omit_words, inv_idx_title, recipes_out)
            if len(ranked_results) == 0:
                all_data = []
            else:
                all_data = ranked_results[:10]
        else:
            all_data = ranked_results[:10]
    return all_data


@irsystem.route('/', methods=['GET'])
def search():
    # obtaining query inputs
    query = request.args.get('search') # for version 1 only
    fav_foods = request.args.get('fav-foods')
    omit_foods = request.args.get('res-foods')
    cal_limit = request.args.get('cal-limit')
    version = request.args.get('version')
    breakfast_selected = request.args.get('breakfast')
    lunch_selected = request.args.get('lunch')
    dinner_selected = request.args.get('dinner')
    drink_included = request.args.get('include-drink')

    if not cal_limit:
        cal_limit = db.session.query(func.max(Recipe.calories)).one()

    # default initialization
    output_message = ''
    breakfast_data = None
    lunch_data = None
    dinner_data = None

    if version is not None and int(version) == 1:
        output_message, data = version_1_search(query, output_message, [])
        return render_template('search-v1.html', name=project_name, netid=net_ids, output_message=output_message, data=data)
    else:
        if fav_foods:
            output_message = "Your search: " + fav_foods

            # basic query cleaning/splitting 
            # (TODO: data validation to check SQL injection and possibly input type)
            fav_foods = fav_foods.lower()
            query_words = fav_foods.split(",")
            query_words = [word.strip() for word in query_words]
            if len(query_words) == 1:
                query_words = query_words[0].split(";")
            """
            for word in query_words:
                query_words.append(word.capitalize())
            """
            omit_words = omit_foods.split(",")
            omit_words = [word.strip() for word in omit_words]
            if len(omit_words) == 1:
                omit_words = omit_words[0].split(";")

            if breakfast_selected is None and lunch_selected is None and dinner_selected is None:
                breakfast_selected = "on"
                lunch_selected = "on"
                dinner_selected = "on"
            if breakfast_selected:
                breakfast_recipes = None # placeholder initialization
                if drink_included:
                    breakfast_recipes = Recipe.query.filter(
                        or_(
                            or_(Recipe.title.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.description.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.ingredients.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.directions.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.categories.like("%{}%".format(word)) for word in query_words),
                        )
                    ).filter_by(calories<cal_limit).filter_by(meal_type="breakfast").all()
                else:
                    breakfast_recipes = Recipe.query.filter(
                        or_(
                            or_(Recipe.title.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.description.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.ingredients.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.directions.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.categories.like("%{}%".format(word)) for word in query_words),
                        )
                    ).filter(Recipe.calories < cal_limit).filter(~Recipe.categories.like("%Drink%")).filter_by(meal_type="breakfast").all()
                breakfast_data = version_2_search(query_words, omit_words, breakfast_recipes)
            if lunch_selected:
                lunch_recipes = None # placeholder initialization
                if drink_included:
                    lunch_recipes = Recipe.query.filter(
                        or_(
                            or_(Recipe.title.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.description.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.ingredients.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.directions.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.categories.like("%{}%".format(word)) for word in query_words),
                        )
                    ).filter_by(meal_type="lunch").all()
                else:
                    lunch_recipes = Recipe.query.filter(
                        or_(
                            or_(Recipe.title.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.description.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.ingredients.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.directions.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.categories.like("%{}%".format(word)) for word in query_words),
                        )
                    ).filter(~Recipe.categories.like("%Drink%")).filter_by(meal_type="lunch").all()
                lunch_data = version_2_search(query_words, omit_words, lunch_recipes)
            if dinner_selected:
                dinner_recipes = None # placeholder initialization
                if drink_included:
                    dinner_recipes = Recipe.query.filter(
                        or_(
                            or_(Recipe.title.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.description.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.ingredients.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.directions.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.categories.like("%{}%".format(word)) for word in query_words),
                        )
                    ).filter_by(meal_type="dinner").all()
                else:
                    dinner_recipes = Recipe.query.filter(
                        or_(
                            or_(Recipe.title.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.description.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.ingredients.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.directions.like("%{}%".format(word)) for word in query_words),
                            or_(Recipe.categories.like("%{}%".format(word)) for word in query_words),
                        )
                    ).filter(~Recipe.categories.like("%Drink%")).filter_by(meal_type="dinner").all()
                dinner_data = version_2_search(query_words, omit_words, dinner_recipes)
            result_success = False
            for data in [breakfast_data, lunch_data, dinner_data]:
                if data is not None and len(data) > 0:
                    result_success = True
                    break
            if not result_success:
                output_message = "No Results Found:("
        return render_template('search-v2.html', name=project_name, 
            netid=net_ids, output_message=output_message, breakfast_data=breakfast_data, 
            lunch_data=lunch_data, dinner_data=dinner_data)
