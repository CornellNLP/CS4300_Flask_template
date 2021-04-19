import json

def merge_sets():
    tv_shows_file = open("datasets/final/tv_shows.json")
    imdb_file = open("datasets/final/imdb.json")

    tv_shows_lst = json.load(tv_shows_file)
    imdb_dict = json.load(imdb_file)

    # with open(tv_shows_file) as json_file:
    #     tv_shows_lst = json.parse(json_file)
    updated_count = 0
    not_updated_count = 0
    for show in tv_shows_lst:
        show_name = show["show_title"]
        if show_name in imdb_dict.keys():
            try:
                updated_count +=1
                imdb_data = imdb_dict[show["show_title"]]
                val = show["show_info"]
                val["genre"] = list(set(val["genre"] + imdb_data["genre"]))
                val["imdb rating"] = imdb_data["rating"]
                val["runtime"] = imdb_data["runtime"]
                val["start year"] = imdb_data["start year"]
                val["end year"] = imdb_data["end year"]
                show["show_info"] = val
                print(show_name + " updated!")
            except Exception as e:
                print(e)
                print("ERROR: " + show_name)
                return
        else:
            not_updated_count+=1
    print("\n" + str(updated_count) + " shows updated")
    print("\n" + str(not_updated_count) + " shows not updated")
    return tv_shows_lst




def main():
    print()
    tv_shows_lst = merge_sets()
    a_file = open("datasets/final/merged_tv_shows.json", "w")
    json.dump(tv_shows_lst, a_file)
    a_file.close()
    print("END OF SCRIPT")



if __name__ == "__main__":
    main()