""" 
Handles all duties related to ingredients 
within the recipe dataset, including 
tokenization and similarity measures.

Author: Liam Daniels
Date: 16 April 2021
"""
import pandas as pd
import numpy as np

ING_CATEGORY_NAME = "ingredients" 

def tokenize_recipe_ingredients(df):
    """
    Given a dataframe of the sampled recipe data,
    replaces that dataframe's ingredients field
    with a list of strings (tokens) instead of a 
    single long string. Also outputs this modified
    dataframe.
    """
    # Space seems like the best delimiter because we
    # want to isolate words like "beef" in ingredients
    # like "ground beef."
    DELIM = " "
    STRIP = "[] ',"

    ing_str_as_list = lambda ing: [s.strip(STRIP) for s in ing.split(DELIM)]
    df[ING_CATEGORY_NAME] = df[ING_CATEGORY_NAME].apply(ing_str_as_list)

    return df

def calc_edit_distance(s1, s2):
    """ Calculates Levenshtein edit distance between two strings"""
    INSERT_COST = 1
    DELETE_COST = 1
    SUB_COST    = 2
    NO_COST     = 0
    sub_func = lambda q, d, i, j: NO_COST if q[i - 1] == d[j - 1] else SUB_COST

    m = len(s1) + 1
    n = len(s2) + 1

    matrix = np.zeros((m, n))
    for i in range(1, m):
            matrix[i, 0] = matrix[i - 1, 0] + DELETE_COST
    for j in range(1, n):
        matrix[0, j] = matrix[0, j - 1] + INSERT_COST
    for i in range(1, m):
        for j in range(1, n):
            matrix[i, j] = min(
                matrix[i - 1, j] + DELETE_COST,
                matrix[i, j - 1] + INSERT_COST, 
                matrix[i - 1, j - 1] + sub_func(s1, s2, i, j) 
            )

    return matrix[-1][-1]

def contains_ingredient(recipe_series, ingredient_query, max_dist=2):
    """
    Checks whether or not a given recipe has an ingredient that
    is within a certain edit distance from the inputted ingredient 
    string. 

    Precondition: ingredients have already been tokenized.

    Parameters:
    -----------------
    recipe_series : pandas.Series
        A row in the recipes dataframe, representing one recipe.

    ingredient_query : str
        The ingredient being checked for within the recipe's ingredients.

    max_dist : int
        The largest edit distance such that two strings are still 
        considered equal.

    Returns:
    ------------------
    bool
        Whether recipe's ingredients contains a token within max_dist of
        the inputted ingredient.
    """
    ingredients = recipe_series[ING_CATEGORY_NAME]
    for ing in ingredients:
        if calc_edit_distance(ing, ingredient_query) <= max_dist:
            return True
    return False

def make_meat_alias_dict(ALIAS_CSV="meat_aliases.csv"):
    """
    Creates dictionary that maps obscure meat parts to their
    common names. Based on specific file structure of a CSV
    that must be in the directory with a specific name.
    """
    with open(ALIAS_CSV) as f:
        lines = f.readlines()
    lines = [l.split(",") for l in lines[1:]]

    aliases = {}
    for l in lines:
        # Element 0 is original name, all others are aliases
        for i in range(1, len(l)):
            alias = l[i].strip()
            original = l[0].strip()
            aliases[alias] = original
    return aliases
