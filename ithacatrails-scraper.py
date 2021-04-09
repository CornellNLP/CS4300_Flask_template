import requests
from bs4 import BeautifulSoup
import re
url = "https://ithacatrails.org/trail/1000"
# url = "https://ithacatrails.org/site/Buttermilk%20Falls%20State%20Park"
# makes a request to the web page and gets its HTML
r = requests.get(url)
# stores the HTML page in 'soup', a BeautifulSoup object
soup = BeautifulSoup(r.content, "html5lib")
# print(soup.prettify())

columns = [
    'Name',
    'Distance',
    'Difficulty',
    'Description',
    'GPS',
    'Parking Locations',
    'Trail Attributes',
    'More info',
]
trail = {}
section = soup.find(True, {"class": "trail-info two-thirds column"})
trail['Name'] = section.find('h1').get_text()
for link in section.find_all('p', limit=2):
    text = link.get_text()
    if text.startswith('Trail distance'):
        trail['Distance'] = float(re.findall(r"[-+]?\d*\.\d+|\d+", text)[0])
    elif text.startswith('Difficulty'):
        trail['Difficulty'] = text.split(": ")[1].split('\n')[0]

# get description

#get gps coords
coords = section.findNext('h3').findNext('p').get_text()
trail['GPS'] = [float(coord) for coord in re.findall(r"[-+]?\d*\.\d+|\d+", coords)] 
# get parking locations
locations = {}
for link in section.findNext(text = 'Parking Locations').findNext('ul').findAll('li'):
    kind, spot = link.get_text().split(': ')[:2]
    kind = kind[:-1].lower()
    spots = locations.get(kind, [])
    spots.append(spot)
    locations[kind] = spots
trail['Parking Locations'] = locations
#get trail attributes
attributes = []
for link in section.findNext(text = 'Trail Attributes').findNext('ul').findAll('li'):
    attributes.append(link.get_text())
trail['Trail Attributes'] = attributes
#get more info
extras = []
for link in section.find('h3', text = 'More Info').findNextSiblings('p', {"class": None}):
    extras.append(" ".join(link.get_text().split()))
trail['More Info'] = extras

def get_trail_names():
    names = []
    url = "https://ithacatrails.org/trail/"
    for id in range(1163, 1394):
        trail_url= url + str(id)
        r = requests.get(trail_url)
        soup = BeautifulSoup(r.content, "html5lib")
        section = soup.find(True, {"class": "trail-info two-thirds column"})
        if section:
            name = section.find('h1').get_text()
            print(str(id) + ": " + str(name))
            names.append(name)
    return names