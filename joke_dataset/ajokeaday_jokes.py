from lxml import html
from lxml.cssselect import CSSSelector
import requests
import json

def extract_jokes(page):
	result = []

	url = 'https://www.ajokeaday.com/jokes/best?page={}'
	response = requests.get(url.format(page))

	sel = CSSSelector('.jubilat p')

	html_elmnts = html.fromstring(response.content)

	for joke in sel(html_elmnts):
		result.append({'joke': joke.text_content().strip(), 'score': None, 'categories': []})

	return result

jokes = []

try:
	for i in range(100):
		joke_lst = extract_jokes(i)
		for joke in joke_lst:
			jokes.append(joke)
finally:
	with open('./json/raw/ajokeaday_jokes_raw.json', 'w') as file:
			json.dump(jokes, file, indent=4)
