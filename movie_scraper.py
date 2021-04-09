import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

headers = {"Accept-Language": "en-US, en;q=0.5"}

baseurl = "https://imsdb.com/scripts/"
url = "https://imsdb.com/all-scripts.html"

results = requests.get(url, headers=headers)

soup = BeautifulSoup(results.text, "html.parser")

movielist = soup.find_all("p")

for p in movielist:
    t = p.findChild("a")
    title = t.get("title")
    script_title = title.replace(" ", "-")
    script_title = script_title[0:-7]
    scripturl = baseurl + script_title + ".html"
    scriptresults = requests.get(scripturl, headers=headers)
    scriptsoup = BeautifulSoup(scriptresults.text, "html.parser")
    script = scriptsoup.find_all("pre")
    

