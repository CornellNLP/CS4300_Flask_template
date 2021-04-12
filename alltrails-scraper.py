import json
import os
import pprint
import requests
import time

# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

"""
Dictionary mapping Ithaca Trails trail names to AllTrails trail ids.
Similar trails on Ithaca Trails will map to the same AllTrails conglomerate trail.
Last updated 4/9/21
"""
NAME_TO_ID = {
    'Bald Hill Trail': None,
    'Beebe Lake Trail - Class of 48 Overlook': None,
    'Beebe Lake Trail - Class of 59 Jogging Trail': None,
    'Beebe Lake Trail - Class of 66 Beebe Beech': None,
    'Beebe Lake Trail - Cowie Beds': None,
    'Beebe Lake Trail - Forest Home Drive': None,
    'Beebe Lake Trail - Fuertes Staircase': None,
    'Beebe Lake Trail - Hemlock Gorge': None,
    'Beebe Lake Trail - Lakeside Path': None,
    'Beebe Lake Trail - Lakeside Path Footbridge': None,
    "Beebe Lake Trail - Sackett's Bridge": None,
    'Beebe Lake Trail - South Rim Connector': None,
    'Beebe Lake Trail - Tang Steps': None,
    'Beebe Lake Trail - Triphammer Falls Bridge': None,
    'Beebe Lake Trail - Triphammer Falls Sidewalk': None,
    'Buttermilk Falls Bear Trail': 10035282,
    'Buttermilk Falls Gorge Connector Trail': None,
    'Buttermilk Falls Gorge Trail': 10354904,
    'Buttermilk Falls Lake Treman Trail': 10684826,
    'Buttermilk Falls Larch Meadow Trail': None,
    'Buttermilk Falls Rim Trail': 10354904,
    'Carl Sagan Planet Walk': None,
    'Cascadilla Gorge Trail - Crescent Entrance': 10673653,
    'Cascadilla Gorge Trail - Eddy Dam Footbridge': 10673653,
    'Cascadilla Gorge Trail - Goldwin Smith Walk': 10673653,
    'Cascadilla Gorge Trail - Hollister Drive Sidewalk': 10673653,
    'Cascadilla Gorge Trail - Hughes Hall': 10673653,
    'Cascadilla Gorge Trail - Lower Gorge': 10673653,
    'Cascadilla Gorge Trail - North Rim': 10673653,
    'Cascadilla Gorge Trail - Oak Avenue': 10673653,
    'Cascadilla Gorge Trail - Rhodes Hall': 10673653,
    'Cascadilla Gorge Trail - Stone Arch Bridge': 10673653,
    'Cascadilla Gorge Trail - Treman Triangle Bridge': 10673653,
    'Cascadilla Gorge Trail - Treman Triangle Footpath': 10673653,
    'Cascadilla Gorge Trail - Trolley Bridge': 10673653,
    'Cascadilla Meadows Trail': None,
    'Cayuga Trail': 10030148,
    'Cayuga Waterfront Trail': 10595923,
    'Cayuga Waterfront Trail (Stewart Park)': 10595923,
    'Cornell Plantations Botanical Garden Paths': None,
    'Dunlop Trail': None,
    'Edwards Lake Cliffs Trail - Lake View': 10665603,
    'Edwards Lake Cliiffs Trail - Loop': 10665603,
    'Edwards Lake Cliiffs Trail - Pocket Falls': 10665603,
    'Ellis Hollow Blue trail': 10299831,
    'Ellis Hollow Red trail': 10299831,
    'Ellis Hollow Wetlands Trail': 10299831,
    'Ellis Hollow Yellow trail': 10299831,
    'F. R. Newman Arboretum Trails': None,
    'Fall Creek Gorge Trail - Chi Psi': None,
    'Fall Creek Gorge Trail - Fall Creek Dr. Rim Trail': None,
    'Fall Creek Gorge Trail - Horseshoe Falls': None,
    'Fall Creek Gorge Trail - North Rim': None,
    'Fall Creek Gorge Trail - North Sidewalk': None,
    'Fall Creek Gorge Trail - Risley': None,
    'Fall Creek Gorge Trail - Suspension Bridge': None,
    'Fall Creek Gorge Trail - University Avenue': None,
    'Fall Creek North Trail': None,
    'Fall Creek South Trail': None,
    'Fall Creek South Trail - Morgan Smith': None,
    # TODO Double-check the Finger Lakes Trails, lots of options on AllTrails
    'Finger Lakes Trail - Buttermilk Falls Finger Lakes Trail': None,
    'Finger Lakes Trail - Hammond Hill FLT': 10267664,
    'Finger Lakes Trail - Lick Brook': 10032393,
    'Finger Lakes Trail - Robert H. Treman CCC Memorial Trail': None,
    'Finger Lakes Trail - Robert H. Treman Finger Lakes Trail/North Country Trail': 10337519,  # Check this
    'Finger Lakes Trail - Robert H. Treman Rim Trail': 10024155,
    'Finger Lakes Trail - Shindagin Hollow FLT': 10017694,
    'Finger Lakes Trail - Stevenson Forest Preserve White trail': 10684836,
    'Finger Lakes Trail - Sweedler White trail': None,
    'Finger Lakes Trail - Tarr-Young': None,
    'Finger Lakes Trail - Thayer Orange trail': None,
    'Fischer Old-growth Forest Trail': None,
    'Floral Ave Multi-Use Facility': None,
    'Frost Ravine Trail': None,
    'Genung Trail': 10686173,
    # TODO Could be the same as Hammond Hill FLT
    'Hammond Hill B1': 10025807,
    'Hammond Hill C2B': 10025807,
    'Hammond Hill G1': 10025807,
    'Hammond Hill G2': 10025807,
    'Hammond Hill G3': 10025807,
    'Hammond Hill R1': 10025807,
    'Hammond Hill R2': 10025807,
    'Hammond Hill S23A': 10025807,
    'Hammond Hill Y1': 10025807,
    'Hammond Hill Y2': 10025807,
    'Hammond Hill Y4': 10025807,
    'Hammond Hill Y4-A': 10025807,
    'Hammond Hill Y5': 10025807,
    'Hammond Hill Y6': 10025807,
    'Hammond Hill Y7': 10025807,
    'Hammond Hill Y8': 10025807,
    'Inlet Island Promenade': None,
    'Ithaca Cemetery - Elm Drive': None,
    'Ithaca Cemetery - Locust Drive': None,
    'Ithaca Cemetery - Maple Drive': None,
    'Ithaca Cemetery - Oak Drive': None,
    'Ithaca Falls': 10032394,
    'Kingsbury Woods Planned trail': 10472911,
    'Lighthouse Point Trail': None,
    'Lindsay-Parsons Blue trail': 10035281,
    'Lindsay-Parsons Red trail': 10035281,
    'Lindsay-Parsons Yellow trail': 10035281,
    'Mann Library Slope Trail': None,
    'Monkey Run Trail': 10662720,
    'Monkey Run Trail - CRC Access': 10662720,
    'Mundy Wildflower Garden Trail': None,
    'Palmer Woods Trail': 10662861,
    'Park Park Trail': None,
    'Polson Trail': None,
    'Purvis Bog Trail': None,
    'Renwick Slope Trail': None,
    'Renwick Wildwoods': None,
    'Ringwood Ponds Trail': None,
    'Robert H. Treman Connector Trail': None,
    'Robert H. Treman Gorge Trail': 10024155,
    'Robert H. Treman Red Pine Trail': None,
    'Robert H. Treman Rim Trail': 10024155,
    'Robert H. Treman Service Road': None,
    'Robert H. Treman Swim Area': 10290032,
    'Robert H. Treman Swim Area Connector': None,
    'Robert H. Treman Unnamed Trail': None,
    'Robert H. Treman Upper Gorge Trail': None,  # TODO
    'Roy H. Park Preserve Blue trail': 10288307,
    'Roy H. Park Preserve Orange trail': 10288307,
    'Roy H. Park Preserve Park Boardwalk': 10288307,
    'Roy H. Park Preserve Park path to Boardwalk': 10288307,
    'Roy H. Park Preserve Park to Hammond Hill': None,  # TODO
    'Roy H. Park Preserve Red trail': 10288307,
    'Shindagin Hollow B1': 10017694,
    'Shindagin Hollow B2': 10017694,
    'Shindagin Hollow B3': 10017694,
    'Shindagin Hollow B4': 10017694,
    'Shindagin Hollow B5': 10017694,
    'Shindagin Hollow B6': 10017694,
    'Shindagin Hollow B7': 10017694,
    'Shindagin Hollow B9': 10017694,
    'Shindagin Hollow C2': 10017694,
    'Shindagin Hollow Entrance': 10017694,
    'Shindagin Hollow G1': 10017694,
    'Shindagin Hollow R1': 10017694,
    'Shindagin Hollow R2': 10017694,
    'Shindagin Hollow R3': 10017694,
    'Shindagin Hollow R4': 10017694,
    'Shindagin Hollow R5': 10017694,
    'Shindagin Hollow R6': 10017694,
    'Shindagin Hollow R7': 10017694,
    'Shindagin Hollow Y1': 10017694,
    'Shindagin Hollow Y2': 10017694,
    'Shindagin Hollow Y3': 10017694,
    'Shindagin Hollow Y3 EXTENSION': 10017694,
    'Shindagin Hollow Y4': 10017694,
    'Shindagin Hollow Y5': 10017694,
    'Shindagin Hollow Y6': 10017694,
    'Shindagin Hollow Y7': 10017694,
    'Shindagin Hollow Y8': 10017694,
    'Shindagin Hollow Y9': 10017694,
    'Six Mile Creek Natural Area': 10030675,
    'Sixmile Creek Walk': 10030675,
    'Slim Jim Woods Trail': None,
    'Stevenson Forest Preserve Blue trail': 10684836,
    'Stevenson Forest Preserve Red trail': 10684836,
    'Stewart Park': 10042562,
    'Sweedler Blue trail': None,
    'Taughannock Falls Gorge Trail': 10021346,
    'Taughannock Falls Multi-use Trail': None,  # TODO
    'Taughannock Falls North Rim Trail': 10297152,
    'Taughannock Falls South Rim Trail': 10297152,
    'Thayer Blue trail': None,
    'Yellow Barn State Forest': None,
}

# Potentially useful API routes:
# https://www.alltrails.com/api/alltrails/trails/10354904/nearby_trails?page=1&per_page=24


def retrieve_review_data_by_trail_id(trail_id):
    """
    Grabs review information through a direct call to AllTrail's API.
    :returns Tuple (TrailName, [Review Dict]) or None if no reviews found
    """
    API_KEY = os.environ.get('ALLTRAILS_API_KEY')
    REVIEWS_URL = f"https://www.alltrails.com/api/alltrails/v2/trails/{str(trail_id)}/reviews"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    URL = REVIEWS_URL + "?key=" + API_KEY
    reviews = []

    r = requests.get(URL, headers=HEADERS)
    res = r.json()

    data = res.get('trail_reviews')
    if data is None:
        return None

    for d in data:
        review = {}
        review['activity'] = None if d['activity'] is None else d['activity']['name']
        review['comment'] = d['comment'].replace("\n", " ").strip() if d['comment'] else ""
        review['obstacles'] = [o['uid'] for o in d['obstacles']]
        review['rating'] = d['rating']
        reviews.append(review)

    return (data[0]['trailName'], reviews)


def reviews_to_json(trail_ids, output_file):
    """
    Given a list of AllTrails trail ids, will output review data per trail into a JSON file.
    """
    out = {}
    for trail_id in trail_ids:
        data = retrieve_review_data_by_trail_id(trail_id)
        if data is None:
            continue
        trail_name, review = data
        out[trail_name] = review

    with open(output_file, "w") as f:
        json.dump(out, f)


def main():
    trail_ids = set(NAME_TO_ID.values())
    reviews_to_json(trail_ids, "alltrails_reviews.json")


if __name__ == "__main__":
    main()

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
