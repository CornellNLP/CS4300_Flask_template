from lxml import html
from lxml.cssselect import CSSSelector
import requests
import json

def extract_jokes():
	result = []
	url = 'https://pun.me/pages/cheesy-pick-up-lines.php'
	response = requests.get(url)

	sel = CSSSelector('ol li')

	html_elmnts = html.fromstring(response.content)

	for joke in sel(html_elmnts):
		result.append({'joke': joke.text_content().strip(), 'score': None, 'categories': ['Pun', 'Pick-up Line']})

	return result

jokes = []

try:
    jokes = extract_jokes()
finally:
	with open('./json/raw/pun_pickup_lines.json', 'w') as file:
			json.dump(jokes, file, indent=4)
