import numpy as np
import googlemaps
import pandas as pd

gmaps = googlemaps.Client(key='AIzaSyC5iZcLzCj7VONadthvLMekcGCVWo-VmKw')

def get_types_synonyms():
    built_in_categories = ['airport','amusement_park','aquarium','art_gallery','atm','bakery','bank','bar',
    'beauty_salon','book_store','cafe','church','dentist','doctor', 'drugstore','food','gym','hair_care','hospital',
    'library','lodging','movie_theater','museum','night_club','park','parking','pharmacy','post_office',
    'restaurant','school','shopping_mall','spa','store','supermarket','university','zoo']

    # synonym dictionary
    synonyms = {}
    synonyms['shopping_mall'] = ['shopping', 'mall']
    synonyms['movie_theater'] = ['movie', 'movie theater','cinema']
    synonyms['lodging'] = ['hotel','inn']
    synonyms['cafe'] = ['coffee','breakfast']
    synonyms['night_club'] = ['club', 'night club']
    synonyms['art_gallery'] = ['art', 'gallery', 'art gallery', 'art museum']
    synonyms['hair_care'] = ['hair', 'hair salon', 'salon']

    return built_in_categories, synonyms

class categoryMismatch(Exception): 
    '''exception for not finding any category match'''
    pass

def match_category(queries):
    '''
    Match an input category with built-in google maps type
    If no match, use "point_of_interest" as the matching category
    Return: (edit distance, category)
    '''
    built_in_categories, synonyms = get_types_synonyms()
    matches = []
    for query in queries:
        match = edit_distance_search(query, built_in_categories, synonyms)
        if match: matches.append(match)
    if len(matches) == 0:
        raise categoryMismatch
    return matches

def update_restult_fields(place, search_function, input_distance=None):
    '''update information fields for one place result'''

    def get_zip_code(coordinate):
            address_components = gmaps.reverse_geocode(coordinate)[0]['address_components']
            if address_components[-1]['types'][0] == 'postal_code':
                zip_code = address_components[-1]['short_name']
            elif address_components[-1]['types'][0] == 'postal_code_suffix':
                zip_code = address_components[-2]['short_name']
            else:
                zip_code = None
            return zip_code

    res = {}
    res['name'] = place['name']
    res['geolocation'] = tuple(place['geometry']['location'].values())
    res['search_method'] = search_function
    res['rating'] = place['rating'] if 'rating' in place else None
    res['price_level'] = place['price_level'] if 'price_level' in place else None
    res['place_id'] = place['place_id']

    if 'types' in place:
        res['types'] = []
        types = place['types']
        for desc in types:
            if desc == 'establishment' or desc == 'point_of_interest':
                continue
            else:
                res['types'].append(desc)
        if (res['types'] == []):
            res['types'] = None
    else:
        res['types'] = None
    
    if search_function == "keyword":
        res['address'] = place['formatted_address']
        res['zip_code'] = res['address'].split(', ')[-2].split(' ')[-1]
    elif search_function == "exact_address":
        res['address'] = place['vicinity']
        res['zip_code'] = get_zip_code(res['geolocation'])
        # res['zip_code'] = gmaps.reverse_geocode(res['geolocation'])[0]['address_components'][-1]['short_name']

    # get distance and duration from origin
    if input_distance: 
        res['distance'] = input_distance['distance']['value']
        res['duration'] = input_distance['duration']['text']
    else:
        res['distance'], res['duration'] = None, None

    res['reviews'] = []
    return res

def edit_distance_search(query, categories, synonyms):
    """ Edit distance search within built-in categories, a match is found if they offset by less than 4

    query: string,The query we are looking for.  
    categories: list of built-in categories in google maps api
    
    Returns result: 
    If there is a category match, return a tuple of edit distance score and matching category like (1.0, 'coffee')
    If there isn't a match, return None
    """
    matches = []
    for category in categories:

        # synonyms of a category
        if category in synonyms:
            extra_categories = synonyms[category]
            for extra_category in extra_categories:
                distance_exta = edit_distance(query, extra_category)
                # print(query, distance_exta)
                # a match is found when distance <= 3
                if distance_exta <= 3:
                    match = (distance_exta, category)
                    matches.append(match)

        distance = edit_distance(query, category)
        # a match is found when distance <= 3
        if distance <= 3:
            match = (distance, category)
            matches.append(match)

    if len(matches) > 0:
        matches.sort(key=lambda x:x[0])
        res = matches[0]
    else:
        res = None
    return res

def insertion_cost(message, j):
    return 1

def deletion_cost(query, i):
    return 1

def substitution_cost(query, message, i, j):
    if query[i-1] == message[j-1]:
        return 0
    else:
        return 2
    
curr_insertion_function = insertion_cost
curr_deletion_function = deletion_cost
curr_substitution_function = substitution_cost

def edit_matrix(query, message):
    """ calculates the edit matrix
    query: query string,
    message: message string,
    
    m: length of query + 1,
    n: length of message + 1,
    
    Returns: edit matrix {(i,j): int}
    """
    
    m = len(query) + 1
    n = len(message) + 1
    
    matrix = np.zeros((m, n))
    for i in range(1, m):
        matrix[i, 0] = matrix[i-1, 0] + curr_deletion_function(query, i)
    
    for j in range(1, n):
        matrix[0, j] = matrix[0, j-1] + curr_insertion_function(message, j)
    
    for i in range(1, m):
        for j in range(1, n):
            matrix[i, j] = min(
                matrix[i-1, j] + curr_deletion_function(query, i), # "down" or delete op
                matrix[i, j-1] + curr_insertion_function(message, j), # "right" or insert op
                matrix[i-1, j-1] + curr_substitution_function(query, message, i, j) # "diagnol" or sub op
            )

    return matrix

def edit_distance(query, message):
    """ Edit distance calculator
    query: query string,       
    message: message string,
    Returns: edit cost (int)
    """
    query = query.lower()
    message = message.lower()
    
    return edit_matrix(query, message)[len(query),len(message)]

def add_reviews(ranked_result):
    results = ranked_result.to_dict('records')
    for res in results:
        place_id = res['place_id']
        place_details = gmaps.place(place_id)['result']
        # res['zip_code'] = place_details['address_components'][-1]['short_name']
        # res['reviews'] = []
        if 'reviews' in place_details:
            reviews = place_details['reviews']
            for review in reviews:
                review_text = {}
                reviewer = review['author_name']
                review_text[reviewer] = review['text']
                res['reviews'].append(review_text)
    return pd.DataFrame(results)

def pre_get_results_keyword(query, category):
    '''
    Get result list using places searching method.
    Input: string query input [query] like "mcdonalds" or "art museum", string [category]
    Output: list of place results 
    '''
    # match input category with one of the built-in categories, if no match change it to "point_of_interest"
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

def pre_get_results_exact_address(address, category, radius):
    '''
    Get result list using place nearby searching method.
    Input: string formatted address [address], int radius [radius] in meters, string [category]
    Output: list of place results
    '''
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
        res_list.append(res)
    return pd.DataFrame(res_list)

def merge_postings(data, categories):
    sim_list = []
    for res in data.index:
        sim_score = 0;
        if data["types"][res] != None:
            A = sorted(data["types"][res])
            B = sorted(categories)
            i = 0
            j = 0
            while i < len(A) and j < len(B):
                if A[i].lower() == B[j].lower():
                    i += 1
                    j += 1
                    sim_score += 1
                else:
                    if A[i] < B[j]:
                        i += 1
                    else:
                        j += 1
        sim_list.append(sim_score)
    data['sim_categories'] = sim_list
    return data
