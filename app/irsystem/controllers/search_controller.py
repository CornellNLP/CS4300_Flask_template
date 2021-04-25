from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import json
import pandas as pd
import numpy as np
import googlemaps

final_data = pd.read_csv("app/static/final_data.csv")
manhattan_modzcta = list(set(final_data['modzcta']))

project_name = "COVID-19 Search Engine"
net_id = "Hogun Lee hl928, Sijin Li sl2624, Irena Gao ijg24, Doreen Gui dg497, Evian Liu yl2867"

def get_results(address, category, radius=100):
    """
    This function extracts a list of location results using Google Map API
    Input: string location, string category, (optional) int radius
    Output: all results of that category within radius, distance from location
    """
    gmaps = googlemaps.Client(key='AIzaSyC5iZcLzCj7VONadthvLMekcGCVWo-VmKw')

    # Geocoding an address
    geocode_result = gmaps.geocode(address)
    # {"sublocality_level_1": "Manhattan", "locality": "New York", "administrative_area_level_1": "NY"})
    origin = geocode_result[0]['geometry']['location']
    # zip_code = geocode_result[0]['address_components'][-1]['short_name']

    # Search nearby open places in a specified category within a radius
    places_result = gmaps.places_nearby(location=origin, radius=radius, type=category, open_now=True)['results']
    # print("Number of results: ", len(places_result))

    # get a list of destination geocodes and compute distances to origin
    geocodes = [tuple(place['geometry']['location'].values()) for place in places_result]
    res_list = []
    if geocodes != []:
        distances = gmaps.distance_matrix(origins=origin, destinations=geocodes)['rows'][0]['elements']

        for i, place in enumerate(places_result):
            res = {}
            res['name'] = place['name']
            res['geolocation'] = tuple(place['geometry']['location'].values())
            if 'rating' in place:
                res['rating'] = place['rating']
            else:
                res['rating'] = None
            res['address'] = place['vicinity']

            # get distance and duration from origin 
            input_distance = distances[i]
            res['distance'] = input_distance['distance']['value']
            res['duration'] = input_distance['duration']['text']

            # get zip code and reviews using place details api
            res['zip_code'] = gmaps.reverse_geocode(res['geolocation'])[0]['address_components'][-1]['short_name']
            res['reviews'] = []
            
#             place_id = place['place_id']
#             place_details = gmaps.place(place_id)['result']
#             res['zip_code'] = place_details['address_components'][-1]['short_name']
#             res['reviews'] = []
#             if 'reviews' in place_details:
#                 reviews = place_details['reviews']
#             else: 
#                 for review in reviews:
#                     review_text = {}
#                     reviewer = review['author_name']
#                     review_text[reviewer] = review['text']
#                     res['reviews'].append(review_text)
                        
            res_list.append(res)
        
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
    
        # merge information onto candidate results by zipcode
        map_result = map_result[map_result.zip_code.astype(int).isin(manhattan_modzcta)] # limit zipcode range for nyc
        map_result['positive_cases'] = map_result.zip_code.astype(int).map(mapping_pos)
        map_result['percent_positive'] = map_result.zip_code.astype(int).map(mapping_percent_pos)
        map_result['full_vax'] = map_result.zip_code.astype(int).map(mapping_vax)
    
    return map_result

def rank_results(data, min_rating=0.0):
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
        n_full_vax = (data.full_vax-data.full_vax.mean())/data.full_vax.std()
        n_percent_positive = (data.percent_positive-data.percent_positive.mean())/data.percent_positive.std()
        if data.rating.isnull().values.any():
            new_rating = data.rating.fillna(2.5)
            n_rating = (new_rating-new_rating.mean())/new_rating.std()
        else:
            n_rating = (data.rating-data.rating.mean())/data.rating.std()
        n_distance = (data.distance-data.distance.mean())/data.distance.std()

        # compute weighted score
        data['score'] = n_full_vax*15.0 - n_percent_positive*7.0 + n_rating*5.0 - n_distance*5.0
        data['score'] = round(data['score'], 4)

        # sort by score
        data = data.sort_values(by='score', ascending=False, na_position='last')
        data = data[data.rating >= min_rating]     # drop results below min_rating if specified

    return data

def get_covid_data(address, category, radius, min_rating):
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
    result = get_results(address, category, radius=100)
    mapped_result = map_covid_vax(result)
    ranked_result = rank_results(mapped_result, min_rating=0.0)

    json_data = ranked_result.to_json(orient="columns")

    return json.loads(json_data)
        

@irsystem.route('/', methods=['GET'])
def search():
    query_int = request.args.get('search_int')
    query_loc = request.args.get('search_loc')
    query_rad = request.args.get('search_rad')
    if not query_int and not query_loc and not query_rad:
        data = []
        output_message = ''
        exists = False
    else:
        output_message = "Your search was point of interest: " + query_int + ", location: " + query_loc + ", radius: " + query_rad
        exists = True
        data = get_covid_data(query_loc, query_int, query_rad, 2.0)

    return render_template('new-search-page.html', name=project_name, netid=net_id, output_message=output_message, data=data, exists=exists)



