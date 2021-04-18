import numpy as np


def inv(x):
    """
    Converts integer scores out of 5 to the inverse. 5 becomes 1, 1 becomes 5,
    etc.
    """
    return 6-x


def generate_personality_vec(legend):
    """
    Ask questions and generate a personality vector for the user.
    """
    p_vec = [0]*len(legend)
    p_vec_count = [0]*len(legend)
    lookup_dict = {}
    for count, i in enumerate(legend):
        lookup_dict[i] = count

    print()
    print("On a scale of 1-5, rate how well the following statements describe you.")

    # charm, social
    print("You are the life of a party.")
    response = int(input("> "))
    p_vec[lookup_dict["Charm"]] += response
    p_vec[lookup_dict["Social"]] += response
    p_vec_count[lookup_dict["Charm"]] += 1
    p_vec_count[lookup_dict["Social"]] += 1

    # social, drive
    print("People near you often rally around you.")
    response = int(input("> "))
    p_vec[lookup_dict["Social"]] += response
    p_vec[lookup_dict["Drive"]] += response
    p_vec_count[lookup_dict["Social"]] += 1
    p_vec_count[lookup_dict["Drive"]] += 1

    # drive, adapt, pragmatic
    print("You will do whatever it takes to succeed, no matter what.")
    response = int(input("> "))
    p_vec[lookup_dict["Drive"]] += response
    p_vec[lookup_dict["Adaptability"]] += response
    p_vec[lookup_dict["Idealistic"]] += inv(response)
    p_vec_count[lookup_dict["Drive"]] += 1
    p_vec_count[lookup_dict["Adaptability"]] += 1
    p_vec_count[lookup_dict["Idealistic"]] += 1

    # sophistication, charm
    print("Your friends come to you for fashion advice.")
    response = int(input("> "))
    p_vec[lookup_dict["Sophistication"]] += response
    p_vec[lookup_dict["Charm"]] += response
    p_vec_count[lookup_dict["Sophistication"]] += 1
    p_vec_count[lookup_dict["Charm"]] += 1

    # prag, kindness
    print("Life is not fair, and that means you have to look out for yourself first and foremost.")
    response = int(input("> "))
    p_vec[lookup_dict["Idealistic"]] += inv(response)
    p_vec[lookup_dict["Kindness"]] += inv(response)
    p_vec_count[lookup_dict["Idealistic"]] += 1
    p_vec_count[lookup_dict["Kindness"]] += 1

    # adapt
    print("You don't like making a plan because you often end up deviating from it anyways.")
    response = int(input("> "))
    p_vec[lookup_dict["Adaptability"]] += response
    p_vec_count[lookup_dict["Adaptability"]] += 1

    # kindness, prag
    print("You see many relationships in your life as transactional.")
    response = int(input("> "))
    p_vec[lookup_dict["Idealistic"]] += inv(response)
    p_vec[lookup_dict["Kindness"]] += inv(response)
    p_vec_count[lookup_dict["Idealistic"]] += 1
    p_vec_count[lookup_dict["Kindness"]] += 1

    # sophistication, adapt
    print("You have high standards of living, and you'll go the extra mile to attain that.")
    response = int(input("> "))
    p_vec[lookup_dict["Sophistication"]] += response
    p_vec[lookup_dict["Adaptability"]] += inv(response)
    p_vec_count[lookup_dict["Sophistication"]] += 1
    p_vec_count[lookup_dict["Adaptability"]] += 1

    for i in range(len(p_vec)):
        p_vec[i] = p_vec[i]/p_vec_count[i]

    print(p_vec)
    return p_vec


# generate_personality_vec([
#    "Charm",
#    "Social",
#    "Idealistic",
#    "Sophistication",
#    "Drive",
#    "Adaptability",
#    "Kindness"
# ])
