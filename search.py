"""
Searches for recipes similar to movie and returns top ten. 
"""
import sim
 
"""
Step 1: generate similarity matrix
Step 2: use movie_name_to_index to retrieve row corresponding to query, or return error if movie not found
Step 3: use index_to_recipe to create list of tuples (similarity score, recipe), sort by similarity score,
return recipes in sorted order
"""