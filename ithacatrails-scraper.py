import requests
from bs4 import BeautifulSoup
import re

TRAIL_ID_INTERVAL = 1000, 1394
START_URL = "https://ithacatrails.org/trail/"
def scrape_trail(section):
    trail = {}

    trail['Name'] = section.find('h1').get_text()
    for link in section.find_all('p', limit=2):
        text = link.get_text()
        if text.startswith('Trail distance'):
            trail['Distance'] = float(re.findall(r"[-+]?\d*\.\d+|\d+", text)[0])
        elif text.startswith('Difficulty'):
            trail['Difficulty'] = text.split(": ")[1].split('\n')[0]

    #get description
    description_link = section.find(text = 'Part of the ').findNext('a').get('href')
    r = requests.get(description_link)
    soup = BeautifulSoup(r.content, "html5lib")
    description_section = soup.find(True, {"class": "trail-info two-thirds column"})
    trail['Description'] = description_section.find_all('p', limit=5)[4].get_text()
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
    return trail

def scrape_all_trails():
    trails = []
    names = set()
    for id in range(TRAIL_ID_INTERVAL[0], TRAIL_ID_INTERVAL[1]):
        trail_url = START_URL + str(id)
        r = requests.get(trail_url)
        soup = BeautifulSoup(r.content, "html5lib")
        section = soup.find(True, {"class": "trail-info two-thirds column"})
        if section:
            name = section.find('h1').get_text()
            if name not in names:
                names.add(name)
                trails.append(scrape_trail(section))
    return trails

def get_trail_names():
    names = set()
    for id in range(TRAIL_ID_INTERVAL[0],TRAIL_ID_INTERVAL[1]):
        trail_url= START_URL + str(id)
        r = requests.get(trail_url)
        soup = BeautifulSoup(r.content, "html5lib")
        section = soup.find(True, {"class": "trail-info two-thirds column"})
        if section:
            names.add(section.find('h1').get_text())
    return sorted(names)

print(get_trail_names())