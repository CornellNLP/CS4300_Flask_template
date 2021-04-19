# from json_reader import json_read_vector
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def inv(x):
    """
    Converts integer scores out of 5 to the inverse. 5 becomes 1, 1 becomes 5,
    etc.
    """
    return 6-x


def prompt():
    """
    Continuously prompts until the user enters a string number between 1 and 5
    inclusive.
    """
    x = input("> ")
    try:
        a = int(x)
        if a < 1 or a > 5:
            raise ValueError("Bad value.")
    except ValueError:
        return prompt()
    else:
        return a


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
    response = prompt()
    p_vec[lookup_dict["Charm"]] += response
    p_vec[lookup_dict["Social"]] += response
    p_vec_count[lookup_dict["Charm"]] += 1
    p_vec_count[lookup_dict["Social"]] += 1

    # social, drive
    print("People near you often rally around you.")
    response = prompt()
    p_vec[lookup_dict["Social"]] += response
    p_vec[lookup_dict["Drive"]] += response
    p_vec_count[lookup_dict["Social"]] += 1
    p_vec_count[lookup_dict["Drive"]] += 1

    # drive, adapt, pragmatic
    print("You will do whatever it takes to succeed, no matter what.")
    response = prompt()
    p_vec[lookup_dict["Drive"]] += response
    p_vec[lookup_dict["Adaptability"]] += response
    p_vec[lookup_dict["Idealistic"]] += inv(response)
    p_vec_count[lookup_dict["Drive"]] += 1
    p_vec_count[lookup_dict["Adaptability"]] += 1
    p_vec_count[lookup_dict["Idealistic"]] += 1

    # sophistication, charm
    print("Your friends come to you for fashion advice.")
    response = prompt()
    p_vec[lookup_dict["Sophistication"]] += response
    p_vec[lookup_dict["Charm"]] += response
    p_vec_count[lookup_dict["Sophistication"]] += 1
    p_vec_count[lookup_dict["Charm"]] += 1

    # prag, kindness
    print("Life is not fair, and that means you have to look out for yourself first and foremost.")
    response = prompt()
    p_vec[lookup_dict["Idealistic"]] += inv(response)
    p_vec[lookup_dict["Kindness"]] += inv(response)
    p_vec_count[lookup_dict["Idealistic"]] += 1
    p_vec_count[lookup_dict["Kindness"]] += 1

    # adapt
    print("You don't like making a plan because you often end up deviating from it anyways.")
    response = prompt()
    p_vec[lookup_dict["Adaptability"]] += response
    p_vec_count[lookup_dict["Adaptability"]] += 1

    # kindness, prag
    print("You see many relationships in your life as transactional.")
    response = prompt()
    p_vec[lookup_dict["Idealistic"]] += inv(response)
    p_vec[lookup_dict["Kindness"]] += inv(response)
    p_vec_count[lookup_dict["Idealistic"]] += 1
    p_vec_count[lookup_dict["Kindness"]] += 1

    # sophistication, adapt
    print("You have high standards of living, and you'll go the extra mile to attain that.")
    response = prompt()
    p_vec[lookup_dict["Sophistication"]] += response
    p_vec[lookup_dict["Adaptability"]] += inv(response)
    p_vec_count[lookup_dict["Sophistication"]] += 1
    p_vec_count[lookup_dict["Adaptability"]] += 1

    for i in range(len(p_vec)):
        p_vec[i] = p_vec[i]/p_vec_count[i]

    return np.array(p_vec)


def similar_varieties(legend, index, mat):
    """
    Takes legend, index, mat, and then prompts user for user personality vector
    and returns a sorted tuple list in the format of (score, wine_variety) in
    order of relevance.
    """
    scores = []
    user = generate_personality_vec(legend)
    for i in range(len(mat)):
        a = cosine_similarity([user], [mat[i]])
        scores.append((a[0][0], index[i]))
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores


def compute_personality_vec(legend, index, mat, responses):
    scores = []

    p_vec = [0]*len(legend)
    p_vec_count = [0]*len(legend)
    lookup_dict = {}
    for count, i in enumerate(legend):
        lookup_dict[i] = count

    # charm, social
    p_vec[lookup_dict["Charm"]] += responses[0]
    p_vec[lookup_dict["Social"]] += responses[0]
    p_vec_count[lookup_dict["Charm"]] += 1
    p_vec_count[lookup_dict["Social"]] += 1

    # social, drive
    p_vec[lookup_dict["Social"]] += responses[1]
    p_vec[lookup_dict["Drive"]] += responses[1]
    p_vec_count[lookup_dict["Social"]] += 1
    p_vec_count[lookup_dict["Drive"]] += 1

    # drive, adapt, pragmatic
    p_vec[lookup_dict["Drive"]] += responses[2]
    p_vec[lookup_dict["Adaptability"]] += responses[2]
    p_vec[lookup_dict["Idealistic"]] += inv(responses[2])
    p_vec_count[lookup_dict["Drive"]] += 1
    p_vec_count[lookup_dict["Adaptability"]] += 1
    p_vec_count[lookup_dict["Idealistic"]] += 1

    # sophistication, charm
    p_vec[lookup_dict["Sophistication"]] += responses[3]
    p_vec[lookup_dict["Charm"]] += responses[3]
    p_vec_count[lookup_dict["Sophistication"]] += 1
    p_vec_count[lookup_dict["Charm"]] += 1

    # prag, kindness
    p_vec[lookup_dict["Idealistic"]] += inv(responses[4])
    p_vec[lookup_dict["Kindness"]] += inv(responses[4])
    p_vec_count[lookup_dict["Idealistic"]] += 1
    p_vec_count[lookup_dict["Kindness"]] += 1

    # adapt
    p_vec[lookup_dict["Adaptability"]] += responses[5]
    p_vec_count[lookup_dict["Adaptability"]] += 1

    # kindness, prag
    p_vec[lookup_dict["Idealistic"]] += inv(responses[6])
    p_vec[lookup_dict["Kindness"]] += inv(responses[6])
    p_vec_count[lookup_dict["Idealistic"]] += 1
    p_vec_count[lookup_dict["Kindness"]] += 1

    # sophistication, adapt
    p_vec[lookup_dict["Sophistication"]] += responses[7]
    p_vec[lookup_dict["Adaptability"]] += inv(responses[7])
    p_vec_count[lookup_dict["Sophistication"]] += 1
    p_vec_count[lookup_dict["Adaptability"]] += 1

    for i in range(len(p_vec)):
        p_vec[i] = p_vec[i]/p_vec_count[i]

    user = np.array(p_vec)

    for i in range(len(mat)):
        a = cosine_similarity([user], [mat[i]])
        scores.append((a[0][0], index[i]))
    scores.sort(key=lambda x: x[0], reverse=True)

    return scores
