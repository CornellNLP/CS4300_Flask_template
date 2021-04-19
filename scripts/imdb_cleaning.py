import pandas as pd
import json
import re


def get_imbd_ds():
    count = 0
    tv_shows_file = 'datasets/TV_info_df.csv'
    df = pd.read_csv(tv_shows_file, na_values='')
    df = df.fillna('')
    result = df.to_dict(orient='records')
    imbd_dict = {}
    
    print(len(result))
    for show in result:
        val = {
            k.lower().strip(): "" if v==-1 or v=="-1" else v
            for k, v in show.items() if k!="Unnamed: 0" and k!= "title" and k!="years"
            }
        val["genre"] = list(val["genre"].split(", "))
        val["rating"] = -1 if val["rating"] == "" else int(val["rating"]) 
        # print(val["runtime"])
        try:
            val["runtime"] = int(val["runtime"][:val["runtime"].index(" ")])
        except:
            val["runtime"] = -1
        # print(show["years"])
        years = show["years"]
        if not any(str.isdigit(c) for c in years):
            val["start year"] = -1
            val["end year"] = -1
        elif bool(re.match(r"\(\D", years)):
            lst = years.split(" ")
            # print(lst)
            x = lst[0][1]
            start_year = lst[1].index("(") + 1
            # print(start_year)
            show["title"] = show["title"] + " " + x
            # print(show["title"])
            # print(lst[1][start_year:lst[1].index("–")])
            try:
                val["start year"] = int(lst[1][start_year:lst[1].index("–")])
            except:
                val["start year"] = int(lst[1][start_year:lst[1].index(")")])
        else:
            start_year = years.index("(") + 1
            # print(years[start_year:years.index("–")])
            try:
                val["start year"] = int(years[start_year:years.index("–")])
            except: 
                val["start year"] = int(years[start_year:years.index(")")])
        try: 
            end_year = years[years.index("–")+1:-1]
            try:
                val["end year"] = int(end_year)
            except:
                val["end year"] = 0
        except:
            val["end year"] = val["start year"]
        if show["title"] in imbd_dict.keys():
            # print(show["title"] +" duplicate")
            # print(imbd_dict[show["title"]])
            # print(val)
            # print()
            count+=1;
            if start_year != 0:
                # print("here")
                new_title = show["title"] + " " + str(start_year)
                imbd_dict[new_title] = val
            else:
                print("ELSE")
        else:
            imbd_dict[show["title"]] = val
    
    # print(count)
    return imbd_dict

        


def main():
    imbd_dict = get_imbd_ds()
    print(len(imbd_dict))
    a_file = open("datasets/final/imdb.json", "w")
    json.dump(imbd_dict, a_file)
    a_file.close()

if __name__ == "__main__":
    main()
