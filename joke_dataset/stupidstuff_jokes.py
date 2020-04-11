from lxml import html
from lxml.cssselect import CSSSelector
import requests
import json
import re

cat_regex = re.compile('(?<=Category: )(.*[A-z])')
scr_regex = re.compile("(?<=Rating: )(.*\d)")

NUM_JOKES = 3773

def extract_joke(id):
	res = {}

	url = 'http://stupidstuff.org/jokes/joke.htm?jokeid={}'
	response = requests.get(url.format(id))

	sel_joke = CSSSelector('.scroll td')
	sel_cat = CSSSelector('center+ .bkline td')

	html_elmnts = html.fromstring(response.content)

	for joke in sel_joke(html_elmnts):
		res['joke'] = joke.text_content().strip()
	for cat in sel_cat(html_elmnts):
		content = cat.text_content().strip()
		category = (cat_regex.search(content)).group(0)
		if (category == 'Miscellaneous'):
			res['categories'] = []
		else: 
			res['categories'] = [category]
		rating = (scr_regex.search(content)).group(0)
		res['score'] = float(rating)
		

	return res

jokes = []

try:
	for i in range(1, NUM_JOKES+1):
		jokes.append(extract_joke(i))

finally:
	with open('./json/raw/stupidstuff_jokes_raw.json', 'w') as file:
		json.dump(jokes, file, indent=4)
