"""
This program makes graphs of the datasets for Q1 of
Project Milestone 2. 
"""

import matplotlib.pyplot as plt
import pandas as pd

def make_dfs():
    RECIPES_FILE = "files/sampled_recipes.csv"
    REVIEWS_FILE = "files/sampled_reviews.csv"
    FOOTPRINT_FILE = "files/Footprint.csv"
    recipe = pd.read_csv(RECIPES_FILE)
    review = pd.read_csv(REVIEWS_FILE)
    footpr = pd.read_csv(FOOTPRINT_FILE)

    # For comparing foods w/ ingredients 
    footpr["Food"] = footpr["Food"].apply(lambda s: s.lower())

    return recipe, review, footpr


def make_recipe_time_histogram():
    rec_df, _, _ = make_dfs()
    mins = rec_df["minutes"]
    mins = mins[mins < 150]

    num_bins = 30
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(mins, num_bins)

    ax.set_xlabel("Cooking time (minutes)")
    ax.set_ylabel("Number of recipes")
    ax.set_title("Histogram of recipe cooking time")

    plt.show()

def make_recipe_desc_length_histogram():
    rec_df, _, _ = make_dfs()
    descl = rec_df["description"]
    descl = descl.apply(lambda x: len(x))
    descl = descl[descl < 1200]

    num_bins = 30
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(descl, num_bins)

    ax.set_xlabel("Description length (characters)")
    ax.set_ylabel("Number of recipes")
    ax.set_title("Histogram of recipe description length")

    plt.show()

def make_review_id_histogram(is_user):
    if is_user:
        word = "user"
        category = "user_id"
    else:
        word = "recipe"
        category = "recipe_id"

    _, rev_df, _ = make_dfs()
    ids = rev_df[category]

    num_bins = ids.nunique()
    print("There are", num_bins, "different {}s!".format(word))
    if is_user:
        ids = ids[ids < 999999]
        num_bins = ids.nunique()
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(ids, num_bins)

    ax.set_ylim([0, 200])
    ax.set_xlabel("{} ID for review".format(word))
    ax.set_ylabel("Number of reviews")
    ax.set_title("Histogram of distinct {}s in reviews".format(word))

    plt.show()

def make_co2_hist():
    _, _, foot = make_dfs()
    carbons = foot["CO2"]

    num_bins = 30
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(carbons, num_bins)

    ax.set_xlabel("CO2 emissions")
    ax.set_ylabel("Number of foods")
    ax.set_title("Histogram of food and their carbon footprints")

    plt.show()

def make_recipe_footprint_histogram():
    rec_df, _, f = make_dfs()

    def calc_co2_from_list(ingredients):
        # This is a bad way of comparing, we should use 
        # edit distance or something later
        calc_co2 = lambda ing : sum(f[f["Food"] == ing]["CO2"])

        # Turn string into list of ingredients.
        # Was going to split on comma, but it's better to split on
        # space because then things like "feta cheese" or "loin lamb"
        # are counted.
        ingredients = ingredients.split(" ")
        ingredients = [s.strip("[] ',") for s in ingredients]

        footprints = [calc_co2(i) for i in ingredients]

        return sum(footprints)

    rec_df = rec_df.head(5000)
    foots = rec_df["ingredients"].apply(calc_co2_from_list)
    foots = foots[foots < 120]

    num_bins = 40
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(foots, num_bins, density=True)

    ax.set_xlabel("CO2")
    ax.set_ylabel("Probability density")
    ax.set_title("Histogram of recipe ingredients' combined CO2 emissions")

    plt.show()

#make_recipe_time_histogram()
make_recipe_footprint_histogram()
#make_review_id_histogram(True)
#make_co2_hist()
#make_recipe_desc_length_histogram()
