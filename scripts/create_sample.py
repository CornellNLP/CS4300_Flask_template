import create_ds as cds

def main():
    (tv_shows, index_to_tv_shows, tv_shows_to_index) = cds.make_tv_show_ds()
    reviews = cds.make_reviews_ds()

    # printing sample output
    print("\n==Printing sample dataset==\n")
    print("Number of TV shows: " + str(len(tv_shows)))
    print("Number of Reviews: " + str(len(reviews)))
    print("\nList of TV Shows with reviews: ")
    for rev in reviews.keys():
        print("\t" + rev)
    print()
    print("##########")
    print("Printing TV shows data")
    for x in range(len(tv_shows)):
        show = tv_shows[x]
        k, val = list(show.keys())[0], list(show.values())[0]
        print("\nSHOW #" + str(x) + ": " + k)
        print("DATA: ")
        for field, v in val.items():
            print(field + ": " + str(v))
        print("----")

    print()
    print("#######")
    print()
    print("Printing sample reviews data")
    for k, v in reviews.items():
        print("\nSHOW: " + k)
        print("REVIEWS: ")
        for title, content in v.items():
            print("Review Title: " + title)
            for x, y in content.items():
                print(x + ": " + str(y))
            print()
        print("----")


if __name__ == "__main__":
    main()