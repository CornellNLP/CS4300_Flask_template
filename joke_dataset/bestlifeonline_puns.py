from lxml import html
from lxml.cssselect import CSSSelector
import requests
import json

def extract_jokes():
    result = []

    url = 'https://bestlifeonline.com/bad-funny-puns/'
    response = requests.get(url)

    sel = CSSSelector('.content li')

    html_elmnts = html.fromstring(response.content)

    for joke in sel(html_elmnts):
        result.append({'joke':joke.text_content().strip(), 'score': None, 'categories': ['Pun']})

    return result

jokes = []

try :
    jokes = extract_jokes()
finally:
    with open('./json/raw/bestlifeonline_puns_raw.json', 'w') as f:
        json.dump(jokes, f, indent=4)
