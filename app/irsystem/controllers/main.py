# Module to call in the terminal to run the IR system.

from json_reader import *
from cosine_similarity import *
from personality_vector import *

print("Welcome to Winetime!")
print("Loading data...")
df = json_read("winemag_data_withtoks.json")
df_personality = json_read("wine_personality.json")
legend, index, mat = json_read_vector("wine_variety_vectors.json")
print("Precomputing resources...")
inv_ind, idf, norms = precompute(df["toks"])

# Personality data
tokenized_personality = tokenizer_personality_data(df_personality)
tokenized_variety = tokenizer_personality_variety(df_personality)
flat_tokenized_variety = flat_tokenizer_personality_variety(df_personality)
inv_ind_person, idf_person, norms_person = precompute_personality(
    tokenized_personality)

print("Load successful!")
print()

quit = False
while not quit:
    print("What is your name? \"quit to exit\"")
    name = input("> ")
    if name == "quit":
        quit = True
        break
    # personality=input("How would your friends describe your personality? ")
    personality = generate_personality_vec(legend)
    print("Describe your favorite drink (can be non-alcoholic!).")
    flavor = input("> ")
    print("Describe your favorite scent.")
    scent = input("> ")
    # q = input("Enter your wine keywords (\"quit\" to exit): ")
    # if name == "quit" or personality == "quit" or flavor == "quit" or scent == "quit":
    #     quit = True
    #     break
    flavor_result = cossim_dict(flavor, inv_ind, idf, norms)
    scent_result = cossim_dict(scent, inv_ind, idf, norms)
    # personality_result=cossim_dict(
    #    personality, inv_ind_person, idf_person, norms_person)
    # personality_result_nondict=cossim(
    #    personality, inv_ind_person, idf_person, norms_person)
    total = total_score(flavor_result, scent_result)
    # a = cossim(q, inv_ind, idf, norms)
    # print(a)
    # display(q, a, df, 10)
    display(name, total, df, 10)
    #display_personality(name, personality_result_nondict, df_personality)

    print()
