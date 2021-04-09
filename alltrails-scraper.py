import pprint
import requests
from bs4 import BeautifulSoup


def test_scrape():
    """
    Testing
    """
    data = []
    URL = "https://www.alltrails.com/trail/us/new-york/buttermilk-falls-gorge-and-rim-trail-loop"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }

    res = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(res.content, 'html5lib')
    reviewBodies = soup.find_all(itemprop="review")

    for body in reviewBodies:
        review = {}

        # Set reviewer name
        review['name'] = body.find(itemprop="name").get_text()

        # Set review description (if any -- optional)
        review_text = body.find(itemprop="reviewBody")
        if review_text is not None:
            review['text'] = review_text.get_text().replace("\n", "")

        # Set review tags (if any -- optional)
        review['tags'] = []
        review_tags = body.find_all(
            "span", class_="styles-module__activityTag___3-RdN")
        if review_tags is not None:
            for tag in review_tags:
                review['tags'].append(tag.get_text())

        # Set review score (out of 5)
        rating_string = body.find(
            "span", class_="MuiRating-root")['aria-label']
        review['rating'] = int(rating_string.split()[0])

        data.append(review)

    return data


pprint.pprint(test_scrape())
