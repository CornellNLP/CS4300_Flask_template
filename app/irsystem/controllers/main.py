# Module to call in the terminal to run the IR system.

from json_reader import json_read
from cosine_similarity import *

print("Welcome to Winetime!")
print("Loading data...")
df = json_read("winemag_data_withtoks.json")
print("Precomputing resources...")
inv_ind, idf, norms = precompute(df["toks"])
print("Load successful!")
print()

quit = False
while not quit:
    q = input("Enter your wine keywords (\"quit\" to exit): ")
    if q == "quit":
        quit = True
        break
    a = cossim(q, inv_ind, idf, norms)
    # print(a)
    display(q, a, df, 10)
    print()
