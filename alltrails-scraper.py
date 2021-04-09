import json
import pprint
import requests
import time

# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

"""
Dictionary mapping Ithaca Trails trail names to AllTrails IDs.
Last updated 4/9/21
"""
ITHACA_TO_ALL_IDS = {
    "Abbott Loop East": 10023212,
    "Abbott Loop West": 10023212,
    "Bald Hill Natural Area": None,
    "Beebe Lake Natural Area": None,
    "Black Diamond Trail": None,
    "Bob Cameron Loop": 10032387,
    "Bock-Harvey Nature Preserve": 10675801,
}


# Potentially useful API routes:
# https://www.alltrails.com/api/alltrails/trails/10354904/nearby_trails?page=1&per_page=24


def test_use_api():
    """
    Grabs review information through a direct call to AllTrail's API.
    """
    # Retrieved from request -> headers -> query string parameters -> "key"
    API_KEY = "3p0t5s6b5g4g0e8k3c1j3w7y5c3m4t8i"
    # Buttermilk Falls Gorge and Rim Trail Loop
    REVIEWS_URL = "https://www.alltrails.com/api/alltrails/v2/trails/10354904/reviews"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    URL = REVIEWS_URL + "?key=" + API_KEY

    r = requests.get(URL, headers=HEADERS)
    res = r.json()
    return [
        {
            "activity": None if d['activity'] is None else d['activity']['name'],
            "comment": d['comment'],
            "obstacles": d['obstacles'],
            "rating": d['rating'],
        }
        for d in res['trail_reviews']]


pprint.pprint(test_use_api())

############ WEB SCRAPING TOOLS ############

# def test_load_results():
#     """
#     Uses selenium to load a specified number of result pages. Used in conjunction with the scraper.
#     Not finished.
#     """
#     drv_path = "./drivers/chromedriver_mac64_v89"
#     driver = webdriver.Chrome(drv_path)
#     # opening the url
#     driver.get(
#         "https://www.alltrails.com/trail/us/new-york/buttermilk-falls-gorge-and-rim-trail-loop")
#     time.sleep(3)
#     button = driver.find_element_by_xpath('//*[@id="reviews"]/div[3]/button')
#     button.send_keys(Keys.ENTER)


# def test_scrape():
#     """
#     Scrapes review data from the Buttermilk Falls Gorge and Rim Trail Loop webpage.

#     :returns A list of dictionaries containing the reviewer name, text, tags, and rating.
#     """
#     data = []
#     URL = "https://www.alltrails.com/trail/us/new-york/buttermilk-falls-gorge-and-rim-trail-loop"
#     HEADERS = {
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
#     }

#     res = requests.get(URL, headers=HEADERS)
#     soup = BeautifulSoup(res.content, 'html5lib')
#     reviewBodies = soup.find_all(itemprop="review")

#     for body in reviewBodies:
#         review = {}

#         # Set reviewer name
#         review['name'] = body.find(itemprop="name").get_text()

#         # Set review description (if any -- optional)
#         review_text = body.find(itemprop="reviewBody")
#         if review_text is not None:
#             review['text'] = review_text.get_text().replace("\n", "")

#         # Set review tags (if any -- optional)
#         review['tags'] = []
#         review_tags = body.find_all(
#             "span", class_="styles-module__activityTag___3-RdN")
#         if review_tags is not None:
#             for tag in review_tags:
#                 review['tags'].append(tag.get_text())

#         # Set review score (out of 5)
#         rating_string = body.find(
#             "span", class_="MuiRating-root")['aria-label']
#         review['rating'] = int(rating_string.split()[0])

#         data.append(review)

#     return data

# test_load_results()
# pprint.pprint(test_scrape())
