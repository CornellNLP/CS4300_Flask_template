from lxml import html
from lxml.cssselect import CSSSelector
import requests
import json

def extract_jokes():
	result = []
	url = 'https://www.quickfunnyjokes.com/computernerd.html'
	response = requests.get(url)

	sel = CSSSelector('.paragraph-text-7')

	html_elmnts = html.fromstring(response.content)

	for joke in sel(html_elmnts):
		lst = joke.text_content().strip().split('\n')
		i = 0
		while i < len(lst):
			tmp = lst[i].strip()
			if len(tmp)!= 0:
				if 'Q:' in tmp:
					result.append({'joke': tmp + '\n ' + (lst[i+1].strip()), 'score': None, 'categories': ['Computers']})
					i += 1
				else:
					result.append({'joke': tmp, 'score': None, 'categories': ['Computers']})
			i += 1

	return result

jokes = []

try:
	jokes = extract_jokes()
	jokes = jokes[1:len(jokes)-1]
finally:
	with open('../json/raw/quickfunnyjokes_comp_jokes.json', 'w') as file:
		json.dump(jokes, file, indent=4)
