from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from flask import request, jsonify
from sqlalchemy import and_, or_
from itertools import combinations
import re

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
    "directions".
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
    # get list of unique tokens
    bofw = set()
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


project_name = "Fitness Dream Team"
net_ids = "Henri Clarke: hxc2, Alice Hu: ath84, Michael Pinelis: mdp93, Genghis Shyy: gs484, Sam Vacura: smv66"

@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    output_message = ''
    data = []
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
                data = ranked_results
                """
                # hardcoding calorie limits; will replace after inputs for calorie limits are added
                grouped_results = group_recipes(ranked_results, recipes_out, 100, 2000)
                if len(grouped_results) == 0:
                    output_message = "No Results Found :((("
                    data = []
                else:
                    output_message = "Your search: " + query
                    data = grouped_results
                """
    return render_template('search.html', name=project_name, netid=net_ids, output_message=output_message, data=data)
