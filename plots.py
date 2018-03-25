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

    genre_counts = dict.fromkeys(labels , 0)

    for movie in data:
        for genre in movie['genres']:
            genre_counts[genre] += 1

    values = list(genre_counts.values())

    draw_hist(labels, values)
