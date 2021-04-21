import numpy as np 

#edit distance functions from my a3
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
    
    Arguments
    =========
    
    query: query string,
        
    message: message string,
    
    m: length of query + 1,
    
    n: length of message + 1,
    
    Returns:
        edit matrix {(i,j): int}
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
    
    Arguments
    =========
    
    query: query string,
        
    message: message string,
    
    Returns:
        edit cost (int)
    """
        
    query = query.lower()
    message = message.lower()
    
    # YOUR CODE HERE
    e_mat = edit_matrix(query, message)
    return e_mat[len(query)][len(message)]

def edit_distance_search(query, msgs):
    """ Edit distance search
    
    Arguments
    =========
    
    query: string,
        The query we are looking for.
        
    msgs: list of dicts,
        Each message in this list has a 'text' field with
        the raw document.
    
    Returns
    =======
    
    result: list of (score, message) tuples.
        The result list is sorted by score such that the closest match
        is the top result in the list.
    
    """
    # YOUR CODE HERE
    result = []
    for m in msgs:
        result.append((edit_distance(query, m), m))
    result.sort(key=lambda x :x[0])
    return result