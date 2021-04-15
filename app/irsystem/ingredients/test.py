import ingredients as ingr
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

def test_all():
    test_tokenize()
    print("All tests pass!")

test_all()
