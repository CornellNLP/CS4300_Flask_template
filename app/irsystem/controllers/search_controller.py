from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import json
import pandas as pd
import numpy as np
import googlemaps
from app.irsystem.controllers.helpers_vague import *

final_data = pd.read_csv("app/static/final_data.csv")
nyc_modzcta = list(set(final_data['modzcta']))

n_full_vax = final_data['%_full_vax'] / final_data['%_full_vax'].max()
n_percent_positive = final_data['%_positive'] / final_data['%_positive'].max()

# updated finaldata with normalization and risk levels computed
final_data["n_risk"] = n_full_vax - n_percent_positive  # risk is % full vax - % positive
risk_labels_5 = ['Very High Risk', 'High Risk', 'Medium Risk', 'Low Risk', 'Very Low Risk']
final_data['risk_level'] = pd.qcut(final_data["n_risk"], q=[0, .2, .4, .6, .8, 1], labels=risk_labels_5)

project_name = "COVID-19 Search Engine"
net_id = "Hogun Lee hl928, Sijin Li sl2624, Irena Gao ijg24, Doreen Gui dg497, Evian Liu yl2867"

def get_results_exact_address(address, category_queries, radius):
    category_matches = match_category(category_queries)
    results = pre_get_results_exact_address(address, category_matches[0], radius)
    for category in category_matches[1:]:
        results = results.append(pre_get_results_exact_address(address, category, radius))
    results.drop_duplicates(subset=["geolocation"], inplace=True)
    results_with_sim = merge_postings(results, [cat[1] for cat in category_matches])
    return results_with_sim

def get_results_keyword(keyword, category_queries):
    category_matches = match_category(category_queries)
    results = pre_get_results_keyword(keyword, category_matches[0])
    for category in category_matches[1:]:
        results = results.append(pre_get_results_keyword(keyword, category))
    results.drop_duplicates(subset=["geolocation"], inplace=True)
    results_with_sim = merge_postings(results, [cat[1] for cat in category_matches])
    return results_with_sim

def map_covid_vax(map_result):
    """
    This function extracts ZIP code from the list of location object that match the specifications listed by the user

    Parameters: {
        locations: list of all locations of the same category and radius - specified by the user
    }
    Requires: candidate results outside exicluded from final_data will have NaN instead
    Returns: dataframe of all results mapped to COVID cases and vaccination data 
    """
    # extract information from datasets
    if not map_result.empty:
        mapping_pos = dict(final_data[['modzcta', 'people_positive']].values)
        mapping_vax = dict(final_data[['modzcta', '%_full_vax']].values)
        mapping_percent_pos = dict(final_data[['modzcta', '%_positive']].values)
        mapping_risk = dict(final_data[['modzcta', "n_risk"]].values)
        mapping_risk_level = dict(final_data[['modzcta', "risk_level"]].values)
        mapping_neighborhood = dict(final_data[['modzcta', 'modzcta_name']].values)
    
        # merge information onto candidate results by zipcode
        map_result = map_result[map_result.zip_code.astype(int).isin(nyc_modzcta)] # limit zipcode range for nyc
        map_result['positive_cases'] = map_result.zip_code.astype(int).map(mapping_pos)
        map_result['percent_positive'] = map_result.zip_code.astype(int).map(mapping_percent_pos)
        map_result['full_vax'] = map_result.zip_code.astype(int).map(mapping_vax)
        map_result['risk'] = map_result.zip_code.astype(int).map(mapping_risk)
        map_result['risk_level'] = map_result.zip_code.astype(int).map(mapping_risk_level)
        map_result['neighborhood'] = map_result.zip_code.astype(int).map(mapping_neighborhood)
    
    return map_result

def rank_results(data, search_option, min_rating=0.0):
    """ 
    This apply all filters to the results: 
    including risk score(covid positive #, positive %, vax %), rating score, …

    Parameters: {
        data: dataset containing descriptions of candidate locations
        min_rating: float, results with lower ratings will be dropped, results w/o ratings will be excluded
    }
    Requires: 
    Returns: dataframe in ranked order
    """
    # normalize columns
    if not data.empty:
        if data.rating.isnull().values.any():
            new_rating = data.rating.fillna(2.5)
            n_rating = new_rating / new_rating.max()
        else:
            n_rating = 0 if data.rating.max() <= 0 else data.rating / data.rating.max()

        if search_option == "exact_address":
            n_distance = 0 if data.distance.max() <= 0 else data.distance / data.distance.max()
        elif search_option == "keyword":
            n_distance = 0

        # compute weighted score
        n_sim_categories = 0 if data['sim_categories'].max() <= 0 else data['sim_categories']/data['sim_categories'].max()
        data['score'] = 2*data['risk'] + n_sim_categories + 0.5*(n_rating - n_distance) 
        data['score'] = round(data['score'], 4)
        # print(data['score'])

        # sort by score
        data = data.sort_values(by='score', ascending=False, na_position='last')
        data = data[data.rating >= min_rating]     # drop results below min_rating if specified

    return data.head(10)

def get_covid_data(category, search_option, location, radius, min_rating):
    """
    This function converts the ranked data in dataframe type to json

    Paramters: {
        ranked_data: dataframe in ranked order
    }
    Requires:
    Returns: json version of the ranked_data
    """
    # json_data = ranked_data.to_json(orient="columns")
    # Need to see the orientation of the dataframe
    # return json_data
    if len(category) == 0: 
        category = 'point_of_interest'
    if search_option == "exact_address" and len(location) > 0:
        result = get_results_exact_address(location, category, radius)
    elif search_option == "keyword" and len(location) > 0:
        result = get_results_keyword(location, category)
    mapped_result = map_covid_vax(result)
    ranked_result = rank_results(mapped_result, search_option, min_rating=0.0)
    final_result = add_reviews(ranked_result)

    # Cap first letter and replace underscore with space
    # for idx in ranked_result['types'].keys():
    #     for t_idx in range(len(ranked_result['types'][idx])):
    #         ranked_result['types'][idx][t_idx] = (ranked_result['types'][idx][t_idx].replace("_", " ")).capitalize()
    
    json_data = ranked_result.to_json(orient="columns")

    return json.loads(json_data)
        

@irsystem.route('/', methods=['GET'])
def search():
    query_rad = request.args.get('search_rad')
    query_cat = request.args.getlist('search_cat')
    query_rat = request.args.get('search_rat')
    query_loc = ""
    search_option = ""
    error = ""
    data = []
    exists = False
    if request.args.get('search_loc') == "":
        query_loc = request.args.get('search_key')
        search_option="keyword"
    elif request.args.get('search_key') == "":
        query_loc = request.args.get('search_loc')
        search_option="exact_address"
    elif request.args.get('search_key') != None and request.args.get('search_loc') != None:
        error = "Only input a specific address (e.g. 20 W 34th St) OR a keyword (e.g. McDonalds)!"
    if error == "" and query_loc != "":
        exists = True
        try:
            data = get_covid_data(query_cat, search_option, query_loc, query_rad, query_rat)
        except categoryMismatch:
            error = "There is no match with the categories you entered, please enter at least one valid category. \n"
            error += "Examples include 'museum','movie theater','bar','restaurant','shopping mall','gym' and so on."

    return render_template('new-search-page.html', name=project_name, netid=net_id, data=data, exists=exists, search_option=search_option, error=error)



