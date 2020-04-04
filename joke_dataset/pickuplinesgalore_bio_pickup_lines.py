from lxml import html
from lxml.cssselect import CSSSelector
import requests
import json

def extract_jokes():
	result = []
	url = 'https://www.pickuplinesgalore.com/biochem.html'
	response = requests.get(url)

	sel = CSSSelector('.paragraph-text-7')

	html_elmnts = html.fromstring(response.content)

	for joke in sel(html_elmnts):
		lst = joke.text_content().strip().split('\n')
		i = 0
		while i < len(lst):
			tmp = lst[i].strip()
			if len(tmp)!= 0:
				result.append({'joke': tmp, 'score': None, 'categories': ['Biology']})
			i += 1

	return result

jokes = []

try:
	jokes = extract_jokes()
	jokes = jokes[1:len(jokes)-1]
finally:
	with open('pickuplinesgalore_bio_pickup_lines.json', 'w') as file:
		json.dump(jokes, file, indent=4)
