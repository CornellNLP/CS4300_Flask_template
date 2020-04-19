from lxml import html
from lxml.cssselect import CSSSelector
import requests
import json
import re

def extract_jokes():
    result = []

    url = 'https://www.sunnyskyz.com/funny-jokes/221/58-Funny-Puns-You-Can-t-Wait-To-Use'
    response = requests.get(url)

    sel = CSSSelector('#picofday p')

    html_elmnts = html.fromstring(response.content)

    for joke in sel(html_elmnts):
        result.append({'joke': joke.text_content().strip(), 'score': None, 'categories': ['Pun']})

    return result

jokes = []

try :
    jokes = extract_jokes()
finally:
    with open('../json/raw/sunnyskyz_puns_raw.json', 'w') as f:
        json.dump(jokes, f, indent=4)
