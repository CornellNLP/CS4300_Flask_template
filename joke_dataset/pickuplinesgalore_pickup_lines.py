from lxml import html
from lxml.cssselect import CSSSelector
import requests
import json

def extract_jokes():
	result = []
	url = 'https://www.pickuplinesgalore.com/cheesy.html'
	response = requests.get(url)

	sel = CSSSelector('.paragraph-text-7')

	html_elmnts = html.fromstring(response.content)

	for joke in sel(html_elmnts):
		lst = joke.text_content().strip().split('\n')
		for i in range(len(lst)):
			if len(lst[i].strip())!= 0:
				result.append({'joke': lst[i].strip(), 'score': None, 'categories': ['Pick-up Line']})
		# result.append({'joke': joke.text_content().strip(), 'score': None, 'categories': []})

	return result

jokes = []

try:
	jokes = extract_jokes()
	jokes = jokes[1:len(jokes)-1]
finally:
	with open('./json/pickuplinesgalore_pickup_lines.json', 'w') as file:
		json.dump(jokes, file, indent=4)
