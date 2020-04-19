from lxml import html
from lxml.cssselect import CSSSelector
import requests
import json
import re

vote_regex = re.compile("(.*\d)")

NUM_JOKES = 99

def extract_jokes():
    result = []

    url = 'https://www.boredpanda.com/funny-dad-jokes-puns/?utm_source=google&utm_medium=organic&utm_campaign=organic'
    response = requests.get(url)

    joke_sel = CSSSelector('.bordered-description')
    vote_sel = CSSSelector('.left .points')

    html_elmnts = html.fromstring(response.content)

    jokes = joke_sel(html_elmnts)
    votes = vote_sel(html_elmnts)

    for i in range(NUM_JOKES):
        joke = jokes[i].text_content().strip()
        vote_raw = votes[i].text_content().strip()
        vote = (vote_regex.search(vote_raw)).group(0)
        result.append({'joke': joke, 'score': int(vote), 'categories': ['Dad Jokes']})

    return result

jokes = None

try :
    jokes = extract_jokes()
finally:
    with open('../json/raw/boredpanda_jokes_raw.json', 'w') as f:
        json.dump(jokes, f, indent=4)
