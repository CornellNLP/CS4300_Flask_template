import scraper as scrap 
from time import sleep

# MAX_SHOWS = 203805
END_SHOWS = 10100

def main():
    for i in range(10001,  END_SHOWS, 200):
        reviews_file = "review_data_" + str(i) + ".csv"
        info_file = "TV_info_df_" + str(i) + ".csv"
        json_file = "review_data_" + str(i) + ".json"
        end = i+200 if i+200 <= END_SHOWS else END_SHOWS
        print("----------")
        print("Scrapping shows from " + str(i) + " to " + str(end))
        print("Files: " + reviews_file + " " + info_file + " " + json_file + "\n")
        scrap.get_data(i, i+200, reviews_file, info_file, json_file)
        sleep(5)
        print("DONE with this part!" + "\n")
    print("\n---------" + "\nEND OF SCRIPT")

if __name__ == "__main__":
    main()