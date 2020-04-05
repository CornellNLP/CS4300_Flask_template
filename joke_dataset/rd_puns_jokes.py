from lxml import html
from lxml.cssselect import CSSSelector
import requests
import json

def extract_jokes(page):
    result = []

    url = 'https://www.rd.com/jokes/puns/page/{}/'
    response = requests.get(url.format(page))

    sel = CSSSelector('#genesis-content p')

    html_elmnts = html.fromstring(response.content)

    for joke in sel(html_elmnts):
        print(joke.text_content())

extract_jokes(1)
