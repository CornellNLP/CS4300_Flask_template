from lxml import html
from lxml.cssselect import CSSSelector
import requests
import json

def extract_jokes(page):
    result = []

    url = 'https://www.rd.com/jokes/puns/page/{}/'
    response = requests.get(url.format(page))

    sel = CSSSelector('.excerpt-wrapper')

    html_elmnts = html.fromstring(response.content)

    for joke in sel(html_elmnts):
        result.append({'joke':joke.text_content().strip(), 'score': None, 'categories': ['Pun']})

    return result

jokes = []

try :
    for i in range(50):
        joke_lst = extract_jokes(i)
        for joke in joke_lst:
            jokes.append(joke)
finally:
    with open('../json/raw/rd_puns_jokes_raw.json', 'w') as f:
        json.dump(jokes, f, indent=4)
