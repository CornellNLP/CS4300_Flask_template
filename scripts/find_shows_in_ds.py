import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import find_starting_letter_links

def makeSoup(url):
    res = session.get(url,timeout=5)
    res.raise_for_status()
    soup_content = BeautifulSoup(res.content, "lxml")
    for style in soup_content(["style"]):
      style.decompose()
    return soup_content

titles_to_links = {}

with open('./datasets/final/tv_shows_to_index.json') as json_file:
  tv_shows_to_index = json.load(json_file)
  tv_shows = list(tv_shows_to_index.keys())
    
  session = requests.Session()

  url = find_starting_letter_links.letters_to_links["M"]
  soup = makeSoup(url)
  show_url = "https://transcripts.foreverdreaming.org"

  for link in soup.select("a.forumlink"):
    title = link.contents[0]
    if title in tv_shows:
      titles_to_links[title] = show_url + link['href'][1:]

print(titles_to_links)
print(len(titles_to_links))
print("\nEND OF SCRIPT")