import numpy as np
import googlemaps

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

def match_category(query):
    '''
    Match an input category with built-in google maps type
    If no match, use "point_of_interest" as the matching category
    Return: (edit distance, category)
    '''
    built_in_categories, synonyms = get_types_synonyms()
    match = edit_distance_search(query, built_in_categories, synonyms)
    if not match:
        # if no match, set edit distance to infinite (1000 here), and default category match to point_of_interest
        match = (1000, 'point_of_interest')
    return match

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
    res['types'] = place['types'] if 'types' in place else None
    
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

