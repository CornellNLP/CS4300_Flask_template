import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os

## REPLACE THIS WITH THE DIRECTORY YOU WANT THE SCRIPTS TO BE DOWNLOADED TO
SCRIPTS_DIR = 'C:/Users/showg/Documents/Scripts'

headers = {"Accept-Language": "en-US, en;q=0.5"}

baseurl = "https://imsdb.com/scripts/"
url = "https://imsdb.com/all-scripts.html"

results = requests.get(url, headers=headers)

soup = BeautifulSoup(results.text, "html.parser")

movielist = soup.find_all("p")

illegal_chars = ["\\", "/", "*", "?", "\"", "<", ">", "|", ":"]
def clean_script(text):
    text = text.replace('Back to IMSDb', '')
    text = text.replace('''<b><!--
</b>if (window!= top)
top.location.href=location.href
<b>// -->
</b>
''', '')
    text = text.replace('''          Scanned by http://freemoviescripts.com
          Formatting by http://simplyscripts.home.att.net
''', '')
    return text.replace(r'\r', '')

for p in movielist:
    t = p.findChild("a")
    title = t.get("title")
    script_title = title.replace(" ", "-")
    file_title = script_title.replace("-", " ")
    script_title = script_title[0:-7]
    print(file_title)
    for c in illegal_chars:
        file_title = file_title.replace(c, "")
    index = len(file_title)
    if " Script" in file_title[-7:]:
        index = file_title.index(" Script")
    if ", The Script" in file_title[-15:]:
        index = file_title.index(", The Script")
    # print(index)
    file_title = file_title[0:index]
    print(file_title)
    scripturl = baseurl + script_title + ".html"
    # print(scripturl)
    scriptresults = requests.get(scripturl, headers=headers)
    scriptsoup = BeautifulSoup(scriptresults.text, "html.parser")
    script = scriptsoup.find_all('td', {'class': "scrtext"})
    if len(script) > 0:
        script = script[0].get_text()
        script = clean_script(script)
        with open(os.path.join(SCRIPTS_DIR, file_title + '.txt'), 'w', encoding='utf-8') as outfile:
                outfile.write(script)
        

