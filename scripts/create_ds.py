# DESCRIPTION: This script creates the data structures using the kaggle data set and the data
# set from the web-scrapping IMDb.
#
# The outline of the data structures for tv_shows and reviews is described in ds.md
#
# DATE: Saturday, April 10, 2021

import pandas as pd

def make_tv_show_ds():
    """
    Returns a tuple of tv_shows, index_to_tv_shows and tv_shows_to_index

    tv_shows is a list of dictionaries represent one tv_show with its data from the kaggle sets.

    index_to_tv_shows is a dictionary with the index as the key and the tv_show as the value (parallel
    to the tv_shows list)

    tv_shows_to_index is a dictionary with the tv_show as the key and the index as the value (parallel
    to the tv_shows list)
    """
    kaggle_file = 'datasets/kaggle_data.csv'
    df = pd.read_csv(kaggle_file, na_values='')
    df = df.fillna('')
    result = df.to_dict(orient='records')

    tv_shows = []
    index_to_tv_shows = {}
    tv_shows_to_index = {}

    for show in result:
        d = {}
        val = {
            k.lower().strip(): "" if v==-1 or v=="-1" else v
            for k, v in show.items() if k!="Unnamed: 0" and k!= "Title" and k!="IMDb"
            }
        val["streaming platform"] = list(val["streaming platform"].replace(",", ", ").split(", "))
        val["genre"] = list(val["genre"].replace(",", ", ").split(", "))
        seasons = val["no of seasons"]
        if seasons!="":
            val["no of seasons"] = int(seasons[0:seasons.index('S')].strip())
        d[show["Title"]] = val
        tv_shows.append(d)
        index_to_tv_shows[show["Unnamed: 0"]] = show["Title"]

    tv_shows_to_index = {v: k for k, v in index_to_tv_shows.items()}
    print("Data structures created for tv shows")
    return (tv_shows, index_to_tv_shows, tv_shows_to_index)


def make_reviews_ds():
    """
    Returns a dictionary of reviews with the tv_show as the key and dictionary of multiple reviews
    for that show as the value.
    """
    imbd_file = 'datasets/TV_reviews_df.csv'
    # get only the columns you want from the csv file
    df = pd.read_csv(imbd_file, na_values='')
    df = df.fillna('')
    result = df.to_dict(orient='records')

    reviews = {}
    for show in result:
        d = {}
        val = {k: "" if v=="NaN" else v for k, v in show.items() if k!="Unnamed: 0" and k!="TV_show" and k!="review_title"}
        if show["TV_show"] not in reviews.keys():
            d[show["review_title"]] = val
            reviews[show["TV_show"]] = d
        else:
            d = reviews[show["TV_show"]]
            d[show["review_title"]] = val
            reviews[show["TV_show"]] = d
    # print(len(reviews))
    # print(reviews["Friends"])
    print("Data structures created for reviews")
    return reviews


def main():
    print()
    (tv_shows, index_to_tv_shows, tv_shows_to_index) = make_tv_show_ds()
    reviews = make_reviews_ds()

    # printing sample output
    print("\n==Printing sample output==\n")
    print("Number of TV shows: " + str(len(tv_shows)))
    print("Number of Reviews: " + str(len(reviews)))
    print("\nList of TV Shows with reviews: ")
    for rev in reviews.keys():
        print("\t" + rev)
    print("\n Example TV show (Friends): ")
    print(tv_shows[tv_shows_to_index["Friends"]])
    print("\n Example review (Friends): ")
    print(reviews["Friends"])


if __name__ == "__main__":
    main()


