import requests
import pandas as pd
from bs4 import BeautifulSoup
import json


def makeSoup(url):
    res = session.get(url,timeout=5)
    res.raise_for_status()
    soup_content = BeautifulSoup(res.content, "lxml")
    for style in soup_content(["style"]):
      style.decompose()
    return soup_content

A_titles_to_links = {}
with open('./datasets/final/tv_shows_to_index.json') as json_file:
  tv_shows_to_index = json.load(json_file)
  tv_shows = list(tv_shows_to_index.keys())
    
  f = 1
  session = requests.Session()

  url = "https://transcripts.foreverdreaming.org/viewforum.php?f=" + str(f)
  soup = makeSoup(url)
  show_url = "https://transcripts.foreverdreaming.org"

  for link in soup.select("a.forumlink"):
    title = link.contents[0]
    if title in tv_shows:
      A_titles_to_links[title] = show_url + link['href'][1:]
