import pandas as pd
import ingredients as ingr
from time import time
DATASET_DIR = "../../../Dataset/files/"
FOOTPRINT_FILE = "{}Footprint.csv".format(DATASET_DIR)
RECIPE_FILE = "{}sampled_recipes.csv".format(DATASET_DIR)
RECIPE_CO2_FILENAME = "recipes_co2_sorted.csv"

def output_co2_df():
    df = pd.read_csv(FOOTPRINT_FILE)
    # For comparing foods w/ ingredients 
    df["Food"] = df["Food"].apply(lambda s: s.lower())
    return df

def calc_ingredients_co2_score(co2_df, ingredients, max_dist=1):
    """
    TODO better documentation
    ingredients is a list of ingredients, already tokenized
    Currently not in use, as this version is significantly
    (over 100x) slower! However, it uses edit distance, which
    means it catches ingredients more easily.
    """
    co2_foods = co2_df["Food"].to_list()

    meat_alias_dict = ingr.make_meat_alias_dict()
    ingredients = [ing if ing not in meat_alias_dict else meat_alias_dict[ing]
                    for ing in ingredients]
    score = 0 
    for food in co2_foods:
        for ing in ingredients:
            if ingr.calc_edit_distance(food, ing) <= max_dist:
                matching_foods = co2_df[co2_df["Food"] == food]
                score += sum(matching_foods["CO2"])

    return score

def calc_ingredients_co2_score_dict(co2_dict, ingredients, max_dist=1):
    """
    TODO better odcumentation here
    ingredients is a list of ingredients, already tokenized
    """
    meat_alias_dict = ingr.make_meat_alias_dict()
    ingredients = [ing if ing not in meat_alias_dict else meat_alias_dict[ing]
                    for ing in ingredients]
    score = 0 
    for ing in ingredients:
        if ing in co2_dict:
            score += co2_dict[ing]

    return score

def make_co2_recipes_csv(df):
    co2_df = output_co2_df()
    co2_dic = {row["Food"] : row["CO2"] for _, row in co2_df.iterrows()}

    t1 = time()

    apply_calc_co2 = lambda x: calc_ingredients_co2_score_dict(co2_dic, x)
    df["CO2"] = df["ingredients"].apply(apply_calc_co2)

    print(df["CO2"])
    print("TIME:", time() - t1, " seconds")

    df = df.sort_values(by="CO2", ascending=True)
    df.to_csv(RECIPE_CO2_FILENAME, 
              columns=["name", "id", "ingredients", "CO2"])
    return df

if __name__ == "__main__":
    df = ingr.tokenize_recipe_ingredients(pd.read_csv(RECIPE_FILE))
    make_co2_recipes_csv(df)
