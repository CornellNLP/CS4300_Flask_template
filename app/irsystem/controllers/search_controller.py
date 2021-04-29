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

n_full_vax = (final_data['%_full_vax'] - final_data['%_full_vax'].mean()) / final_data['%_full_vax'].std()
n_percent_positive = (final_data['%_positive'] - final_data['%_positive'].mean()) / final_data['%_positive'].std()

# updated finaldata with normalization and risk levels computed
final_data["n_risk"] = n_full_vax - n_percent_positive  # risk is % full vax - % positive
risk_labels_5 = ['Very High Risk', 'High Risk', 'Median Risk', 'Low Risk', 'Very Low Risk']
final_data['risk_level'] = pd.qcut(final_data["n_risk"], q=[0, .2, .4, .6, .8, 1], labels=risk_labels_5)

project_name = "COVID-19 Search Engine"
net_id = "Hogun Lee hl928, Sijin Li sl2624, Irena Gao ijg24, Doreen Gui dg497, Evian Liu yl2867"

def get_results_exact_address(address, category, radius):
    '''
    Get result list using place nearby searching method.
    Input: string formatted address [address], int radius [radius] in meters, string [category]
    Output: list of place results
    '''
    # match input category with one of the built-in categories, if no match change it to "point_of_interest"
    category = match_category(category)[1]

     # Geocoding an address
    geocode_result = gmaps.geocode(address)
    # {"sublocality_level_1": "Manhattan", "locality": "New York", "administrative_area_level_1": "NY"})
    
    origin = geocode_result[0]['geometry']['location']

    # Search nearby open places in a specified category within a radius
    # places_result = gmaps.places_nearby(location=origin, radius=radius, type=category, open_now=True)['results']
    places_result = gmaps.places_nearby(location=origin, radius=radius, type=category)['results']


    # get a list of destination geocodes and compute distances to origin
    geocodes = [tuple(place['geometry']['location'].values()) for place in places_result]
    res_list = []
    if geocodes != []:
        distances = gmaps.distance_matrix(origins=origin, destinations=geocodes)['rows'][0]['elements']
    
    res_list = []
    for i, place in enumerate(places_result):
        business_status = place['business_status'] if 'business_status' in place else "OPERATIONAL"
        if business_status != "OPERATIONAL":
            continue
        if distances:
            input_distance = distances[i]
        else:
            input_distance = None
        res = update_restult_fields(place, "exact_address", input_distance=input_distance)
        
        # TODO: REPLACE WITH ACTUAL PRICE LEVEL
        res['price_level'] = np.random.randint(1,4)
        res['reviews'] = [
            {'Name 1': 'REPLACE ME WITH ACTUAL REVIEWS'},
            {'Name 2': 'PLACEHOLDER FOR TESTING'}
        ]
        
        res_list.append(res)
    return pd.DataFrame(res_list)

def get_results_keyword(query, category):
    '''
    Get result list using places searching method.
    Input: string query input [query] like "mcdonalds" or "art museum", string [category]
    Output: list of place results 
    '''
    # match input category with one of the built-in categories, if no match change it to "point_of_interest"
    category = match_category(category)[1]

    def within_nyc(address):
        city = address.split(", ")[-3]
        return (city == "New York")

    # latitude, longitude for the center of manhattan 
    nyc_latlog = (40.758896, -73.985130)
    places_results = gmaps.places(query=query,location=nyc_latlog, radius=30000)["results"]

    res_list = []
    for i, place in enumerate(places_results):
        business_status = place['business_status'] if 'business_status' in place else "OPERATIONAL"
        address = place['formatted_address']
        if within_nyc(address) and business_status == "OPERATIONAL":
            res = update_restult_fields(place, "keyword")
            res_list.append(res)
            # updated_places.append(place)
    return pd.DataFrame(res_list)

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
    
        # merge information onto candidate results by zipcode
        map_result = map_result[map_result.zip_code.astype(int).isin(nyc_modzcta)] # limit zipcode range for nyc
        map_result['positive_cases'] = map_result.zip_code.astype(int).map(mapping_pos)
        map_result['percent_positive'] = map_result.zip_code.astype(int).map(mapping_percent_pos)
        map_result['full_vax'] = map_result.zip_code.astype(int).map(mapping_vax)
        map_result['risk'] = map_result.zip_code.astype(int).map(mapping_risk)
        map_result['risk_level'] = map_result.zip_code.astype(int).map(mapping_risk_level)
    
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
            n_rating = 0 if round(new_rating.std(),4)==0 else (new_rating-new_rating.mean())/new_rating.std()
        else:
            n_rating = 0 if round(data.rating.std(),4)==0 else (data.rating-data.rating.mean())/data.rating.std()
        if search_option == "exact_address":
            n_distance = 0 if round(data.distance.std(),4)==0 else (data.distance-data.distance.mean())/data.distance.std()
        elif search_option == "keyword":
            n_distance = 0

        # compute weighted score
        data['score'] = 2*data['risk'] + n_rating - n_distance
        data['score'] = round(data['score'], 4)
        # print(data['score'])

        # sort by score
        data = data.sort_values(by='score', ascending=False, na_position='last')
        data = data[data.rating >= min_rating]     # drop results below min_rating if specified

    return data

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
    if search_option == "exact_address" and len(location) > 0:
        result = get_results_exact_address(location, category, radius)
    elif search_option == "keyword" and len(location) > 0:
        result = get_results_keyword(location, category)
    mapped_result = map_covid_vax(result)
    ranked_result = rank_results(mapped_result, search_option, min_rating=0.0)

    # Cap first letter and replace underscore with space
    for idx in ranked_result['types'].keys():
        for t_idx in range(len(ranked_result['types'][idx])):
            ranked_result['types'][idx][t_idx] = (ranked_result['types'][idx][t_idx].replace("_", " ")).capitalize()
    
    json_data = ranked_result.to_json(orient="columns")

    return json.loads(json_data)
        

@irsystem.route('/', methods=['GET'])
def search():
    query_rad = request.args.get('search_rad')
    query_cat = request.args.getlist('search_cat')
    query_loc = ""
    if request.args.get('search_loc') == "":
        query_loc = request.args.get('search_key')
        search_option="keyword"
    elif request.args.get('search_key') == "":
        query_loc = request.args.get('search_loc')
        search_option="exact_address"
    if not query_loc and not query_rad:
        data = []
        output_message = ''
        exists = False
    else:
        output_message = "Your search was point of interest: , location: " + query_loc + ", radius: " + query_rad
        exists = True
        data = get_covid_data(query_cat[0], search_option, query_loc, query_rad, 2.0)

    return render_template('new-search-page.html', name=project_name, netid=net_id, output_message=output_message, data=data, exists=exists)



