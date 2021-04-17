import requests
from requests import get
import re
import json

from time import sleep
from random import randint
import pandas as pd

from bs4 import BeautifulSoup



def tag_contents(tag, type):
    """
    Return the text inside the html tag block in string format
    """
    tag = str(tag)

    t_si = tag.find('>')
    t_ei = tag.find('</' + type + '>', t_si)

    return tag[t_si+1: t_ei]

def get_helpful(tag):
    """
    Return the text inside the html tag block in string format
    """
    tag = str(tag)

    t_si = tag.find("\n")
    t_ei = tag.find("\n", t_si+1)

    return tag[t_si+1: t_ei].strip()

def get_rating_span(span):
    """
    Return the text inside the html tag block in string format
    """
    span = str(span)

    span_tag_start = span.find('<span>')
    sp_si = span.find('>', span_tag_start)
    sp_ei = span.find('</span>', sp_si)

    return span[sp_si+1: sp_ei]


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)\
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}

dict_of_shows = {}

TV_show = []
reviews_title = []
reviews_content = []
reviews_helpful = []
reviews_rating = []
reviews_date = []


for num in range(1, 2001, 50):
    print(num)
    sleep(randint(1,5))
    TV_shows = get('https://www.imdb.com/search/title/?title_type=tv_series&start=1&ref_=adv_nxt',
    headers = headers)
    print(TV_shows.status_code) #prints 200 if successful


    laptop_soup = BeautifulSoup(TV_shows.content, 'html.parser')

    container = laptop_soup.find_all('h3', class_ = "lister-item-header")

    show_reviews_list = []

    for show_link in container:
        link = str(show_link.find_all('a')[0])
        link_si = link.find('"')
        link_ei = link.find('?', link_si+1)

        title = tag_contents(link, "a")



        link = link[link_si+1: link_ei]

        show_reviews_link = "https://www.imdb.com" + link + "reviews?ref_=tt_urv"
        show_reviews_list.append(show_reviews_link)

        sleep(randint(1,5))
        show_reviews = get(show_reviews_link, headers = headers)
        review_soup = BeautifulSoup(show_reviews.content, 'html.parser')

        review_list = review_soup.find_all('div', class_ = "review-container")
        review_info_list = []
        for rev in review_list:

            end = tag_contents(rev.find_all('a', class_ = "title")[0], "a").find("\n")
            review_title = tag_contents(rev.find_all('a', class_ = "title")[0], "a")[:end]

            review_content = tag_contents(rev.find_all('div', class_ = "text show-more__control")[0], "div")
            review_helpful = get_helpful(rev.find_all('div', class_ = "actions text-muted")[0])

            rev_rating = rev.find_all('span', class_ = "rating-other-user-rating")
            if len(rev_rating) == 0:
                review_rating = None
            else:
                review_rating = int(get_rating_span(rev_rating[0]))

            review_date = tag_contents(rev.find_all('span', class_ = "review-date")[0], "span")

            review_info_list.append({'title': review_title, 'content': review_content, 'rating': review_rating, \
            'helpful': review_helpful, 'date': review_date})

            #dataframe column lists
            TV_show.append(title)
            reviews_title.append(review_title)
            reviews_content.append(review_content)
            reviews_helpful.append(review_helpful)
            reviews_rating.append(review_rating)
            reviews_date.append(review_date)

        dict_of_shows[link] = {'title': title, 'reviews': review_info_list}

TV_reviews_df = pd.DataFrame({"TV_show": TV_show,
"review_title": reviews_title,
"review_content": reviews_content,
"review_helpful": reviews_helpful,
"review_rating": reviews_rating,
"review_date": reviews_date})

TV_reviews_df.to_csv("datasets/TV_reviews_df.csv")

a_file = open("datasets/review_data.json", "w")
json.dump(dict_of_shows, a_file)
a_file.close()
