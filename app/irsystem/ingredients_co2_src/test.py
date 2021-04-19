import ingredients as ingr
import co2_handling as co2
import pandas as pd

DATASET_DIR = "../../../Dataset/files/"
RECIPE_FILE = "{}sampled_recipes.csv".format(DATASET_DIR)

def test_eq(name, output, expected):
    error_str = "{}: expected {}, but got {}.".format(name, expected, output)
    assert output == expected, error_str

def test_tokenize():
    tests = [
        ("First recipe, first ing", 0, 0, "water"),
        ("Spicy jerky: separate soy from sauce", 13, 1, "soy"),
        ("Oranges, zest of", 24, 6, "zest"),
        ("Last in ingredient list", 62, 17, "vanilla"),
        ("Hyphen in word", 87, 7, "all-purpose")
    ]

    df = ingr.tokenize_recipe_ingredients(pd.read_csv(RECIPE_FILE))
    def test_by_loc(name, rec_idx, ing_idx, expected):
        output = df.loc[rec_idx]["ingredients"][ing_idx]
        test_eq(name, output, expected)
    for t in tests: test_by_loc(t[0], t[1], t[2], t[3])

def test_edit_distance():
    tests = [
        ("Egg and eggs", "egg", "eggs", 1),
        ("Eggs and eggz", "eggs", "eggz", 2),
        ("Eggs and egg", "eggs", "egg", 1),
        ("Kardashian dalmatian", "kardashian", "dalmatian", 9)
    ]

    for t in tests: 
        output = ingr.calc_edit_distance(t[1], t[2])
        expected = t[3]
        name = t[0]
        test_eq(name, output, expected)

def test_contains_ingredient():
    tests = [
        ("First rec contains water", 0, "water", 2, True),
        ("First rec doesn't contain beef", 0, "beef", 2, False),
        ("First rec contains dates", 0, "dates", 2, True),
        ("First rec contains date", 0, "date", 2, True),
        ("First rec contains dat", 0, "dat", 2, True),
        ("First rec doesn't contains tate", 0, "tate", 2, False)
    ]

    df = ingr.tokenize_recipe_ingredients(pd.read_csv(RECIPE_FILE))
    for t in tests:
        name = t[0]
        series = df.loc[t[1]]
        query = t[2]
        max_dist = t[3]
        expected = t[4]
        output = ingr.contains_ingredient(series, query, max_dist)
        test_eq(name, output, expected)
        
def test_meat_aliases():
    tests = [
        ("chuck is beef", "chuck", "beef"),
        ("loin is beef", "loin", "beef"),
        ("hock is pork", "hock", "pork")
    ]

    meat = ingr.make_meat_alias_dict()
    for t in tests:
        output = meat[t[1]]
        name = t[0]
        expected = t[2]
        test_eq(name, output, expected)

def test_food_co2():
    tests = [
        ("Beef has 44", ["beef"], 44)
    ]

    df = co2.output_co2_df()
    for t in tests:
        output = int(co2.calc_ingredients_co2_score(df, t[1]))
        test_eq(t[0], output, t[2])

def test_food_filter():
    tests = [
        ("No water", ["water"], 0, 26946)
    ]
    for t in tests:
        df = ingr.tokenize_recipe_ingredients(pd.read_csv(RECIPE_FILE))
        df = df.head(100)
        name = t[0]
        banned = t[1]
        idx = t[2]
        expected = t[3]
        df = ingr.filter_foods(t[1], df, 2)
        print(df)
        test_eq(name, df.loc[idx]["id"], expected)

def test_all():
    test_tokenize()
    test_edit_distance()
    test_contains_ingredient()
    test_meat_aliases()
    test_food_co2()
    test_food_filter()
    print("All tests pass!")

test_all()
