""" 
Handles all duties related to ingredients 
within the recipe dataset, including 
tokenization and similarity measures.

Author: Liam Daniels
Date: 15 April 2021
"""
import pandas as pd

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
    ING_CATEGORY_NAME = "ingredients" 
    STRIP = "[] ',"

    ing_str_as_list = lambda ing: [s.strip(STRIP) for s in ing.split(DELIM)]
    df[ING_CATEGORY_NAME] = df[ING_CATEGORY_NAME].apply(ing_str_as_list)

    return df

