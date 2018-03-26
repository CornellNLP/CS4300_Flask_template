import json
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

def draw_hist(labels, values):
    indices = np.arange(len(labels))
    width = 5
    plt.bar(indices*5, values, width)
    plt.xticks(indices*5, labels, rotation=70)
    plt.show()

if __name__ == "__main__":
    data = []
    with open("movies.json") as f:
        data = json.load(f)

    labels = ["Action", "Adventure","Animation","Comedy","Crime","Documentary","Drama",
    "Family","Fantasy", "History","Horror","Music","Mystery","Romance","Science Fiction",
    "TV Movie","Thriller","War","Western"]

    genre_counts = dict.fromkeys(labels, 0)

    for movie in data:
        for genre in movie['genres']:
            genre_counts[genre] += 1

    # key labels and values in the same order
    keylist = genre_counts.keys()
    keylist.sort()
    values = [genre_counts[key] for key in keylist]

    # get counts for overview length
    overview_counts = dict()
    for movie in data:
        length = (len(movie['overview'].split()) - 1)/10
        if length not in overview_counts:
            overview_counts[length] = 1
        else:
            overview_counts[length] += 1

    # get counts for release year
    release_counts = dict()
    for movie in data:
        release = int(movie['release_date'][:4])
        decade = (release + 1)/10
        if decade not in release_counts:
            release_counts[decade] = 1
        else:
            release_counts[decade] += 1

    draw_hist(labels, values)
