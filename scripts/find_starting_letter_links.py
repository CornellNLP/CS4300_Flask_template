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

letters_to_links = {}
    
session = requests.Session()

url = "https://transcripts.foreverdreaming.org"
soup = makeSoup(url)

for link in soup.select("a.forumlink"):
  letter = link.contents[0]
  link = url + link['href'][1:]
  letters_to_links[letter] = link

print("\nEND OF SCRIPT")