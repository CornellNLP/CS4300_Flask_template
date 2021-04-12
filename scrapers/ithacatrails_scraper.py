import requests
from bs4 import BeautifulSoup
import re
import json
from alltrails_scraper import NAME_TO_ID

# print(len(NAME_TO_ID))
TRAIL_ID_INTERVAL = 1000, 1394
START_URL = "https://ithacatrails.org/trail/"
NAMES_WITH_BOTH_ID = {'Ellis Hollow Yellow trail': {'ithaca': 1000, 'alltrails': 10299831}, 'Ellis Hollow Red trail': {'ithaca': 1001, 'alltrails': 10299831}, 'Ellis Hollow Blue trail': {'ithaca': 1002, 'alltrails': 10299831}, 'Kingsbury Woods Planned trail': {'ithaca': 1003, 'alltrails': 10472911}, 'Roy H. Park Preserve Blue trail': {'ithaca': 1004, 'alltrails': 10288307}, 'Roy H. Park Preserve Orange trail': {'ithaca': 1005, 'alltrails': 10288307}, 'Roy H. Park Preserve Red trail': {'ithaca': 1006, 'alltrails': 10288307}, 'Roy H. Park Preserve Park Boardwalk': {'ithaca': 1007, 'alltrails': 10288307}, 'Roy H. Park Preserve Park path to Boardwalk': {'ithaca': 1008, 'alltrails': 10288307}, 'Lindsay-Parsons Blue trail': {'ithaca': 1013, 'alltrails': 10035281}, 'Lindsay-Parsons Red trail': {'ithaca': 1016, 'alltrails': 10035281}, 'Lindsay-Parsons Yellow trail': {'ithaca': 1017, 'alltrails': 10035281}, 'Stevenson Forest Preserve Blue trail': {'ithaca': 1023, 'alltrails': 10684836}, 'Finger Lakes Trail - Stevenson Forest Preserve White trail': {'ithaca': 1024, 'alltrails': 10684836}, 'Stevenson Forest Preserve Red trail': {'ithaca': 1025, 'alltrails': 10684836}, 'Genung Trail': {'ithaca': 1026, 'alltrails': 10686173}, 'Cayuga Trail': {'ithaca': 1274, 'alltrails': 10030148}, 'Edwards Lake Cliiffs Trail - Pocket Falls': {'ithaca': 1226, 'alltrails': 10665603}, 'Edwards Lake Cliiffs Trail - Loop': {'ithaca': 1236, 'alltrails': 10665603}, 'Edwards Lake Cliffs Trail - Lake View': {'ithaca': 1227, 'alltrails': 10665603}, 'Finger Lakes Trail - Lick Brook': {'ithaca': 1081, 'alltrails': 10032393}, 'Cascadilla Gorge Trail - North Rim': {'ithaca': 1240, 'alltrails': 10673653}, 'Cascadilla Gorge Trail - Eddy Dam Footbridge': {'ithaca': 1085, 'alltrails': 10673653}, 'Cascadilla Gorge Trail - Goldwin Smith Walk': {'ithaca': 1086, 'alltrails': 10673653}, 'Cascadilla Gorge Trail - Oak Avenue': {'ithaca': 1093, 'alltrails': 10673653}, 'Cascadilla Gorge Trail - Rhodes Hall': {'ithaca': 1090, 'alltrails': 10673653}, 'Cascadilla Gorge Trail - Treman Triangle Footpath': {'ithaca': 1098, 'alltrails': 10673653}, 'Cascadilla Gorge Trail - Lower Gorge': {'ithaca': 1180, 'alltrails': 10673653}, 'Cascadilla Gorge Trail - Stone Arch Bridge': {'ithaca': 1100, 'alltrails': 10673653}, 'Cascadilla Gorge Trail - Treman Triangle Bridge': {'ithaca': 1101, 'alltrails': 10673653}, 'Ellis Hollow Wetlands Trail': {'ithaca': 1106, 'alltrails': 10299831}, 'Monkey Run Trail': {'ithaca': 1231, 'alltrails': 10662720}, 'Cascadilla Gorge Trail - Trolley Bridge': {'ithaca': 1127, 'alltrails': 10673653}, 'Palmer Woods Trail': {'ithaca': 1158, 'alltrails': 10662861}, 'Monkey Run Trail - CRC Access': {'ithaca': 1259, 'alltrails': 10662720}, 'Cascadilla Gorge Trail - Crescent Entrance': {'ithaca': 1169, 'alltrails': 10673653}, 'Cascadilla Gorge Trail - Hughes Hall': {'ithaca': 1186, 'alltrails': 10673653}, 'Cascadilla Gorge Trail - Hollister Drive Sidewalk': {'ithaca': 1222, 'alltrails': 10673653}, 'Taughannock Falls South Rim Trail': {'ithaca': 1275, 'alltrails': 10297152}, 'Buttermilk Falls Bear Trail': {'ithaca': 1278, 'alltrails': 10035282}, 'Taughannock Falls Gorge Trail': {'ithaca': 1279, 'alltrails': 10021346}, 'Taughannock Falls North Rim Trail': {'ithaca': 1281, 'alltrails': 10297152}, 'Buttermilk Falls Gorge Trail': {'ithaca': 1282, 'alltrails': 10354904}, 'Robert H. Treman Gorge Trail': {'ithaca': 1284, 'alltrails': 10024155}, 'Robert H. Treman Swim Area': {'ithaca': 1291, 'alltrails': 10290032}, 'Buttermilk Falls Lake Treman Trail': {'ithaca': 1317, 'alltrails': 10684826}, 'Robert H. Treman Rim Trail': {'ithaca': 1320, 'alltrails': 10024155}, 'Finger Lakes Trail - Robert H. Treman Rim Trail': {'ithaca': 1319, 'alltrails': 10024155}, 'Buttermilk Falls Rim Trail': {'ithaca': 1321, 'alltrails': 10354904}, 'Finger Lakes Trail - Robert H. Treman Finger Lakes Trail/North Country Trail': {'ithaca': 1325, 'alltrails': 10337519}, 'Hammond Hill G3': {'ithaca': 1326, 'alltrails': 10025807}, 'Hammond Hill G1': {'ithaca': 1327, 'alltrails': 10025807}, 'Hammond Hill C2B': {'ithaca': 1328, 'alltrails': 10025807}, 'Hammond Hill B1': {'ithaca': 1329, 'alltrails': 10025807}, 'Hammond Hill R1': {'ithaca': 1330, 'alltrails': 10025807}, 'Hammond Hill R2': {'ithaca': 1331, 'alltrails': 10025807}, 'Hammond Hill Y6': {'ithaca': 1332, 'alltrails': 10025807}, 'Hammond Hill Y4': {'ithaca': 1333, 'alltrails': 10025807}, 'Hammond Hill S23A': {'ithaca': 1334, 'alltrails': 10025807}, 'Hammond Hill Y2': {'ithaca': 1341, 'alltrails': 10025807}, 'Hammond Hill Y8': {'ithaca': 1336, 'alltrails': 10025807}, 'Hammond Hill G2': {'ithaca': 1337, 'alltrails': 10025807}, 'Hammond Hill Y5': {'ithaca': 1338, 'alltrails': 10025807}, 'Hammond Hill Y7': {'ithaca': 1339, 'alltrails': 10025807}, 'Hammond Hill Y4-A': {'ithaca': 1340, 'alltrails': 10025807}, 'Hammond Hill Y1': {'ithaca': 1342, 'alltrails': 10025807}, 'Finger Lakes Trail - Hammond Hill FLT': {'ithaca': 1344, 'alltrails': 10267664}, 'Shindagin Hollow R1': {'ithaca': 1345, 'alltrails': 10017694}, 'Shindagin Hollow R2': {'ithaca': 1346, 'alltrails': 10017694}, 'Shindagin Hollow R3': {'ithaca': 1347, 'alltrails': 10017694}, 'Shindagin Hollow R4': {'ithaca': 1348, 'alltrails': 10017694}, 'Shindagin Hollow R5': {'ithaca': 1349, 'alltrails': 10017694}, 'Shindagin Hollow R6': {'ithaca': 1350, 'alltrails': 10017694}, 'Shindagin Hollow R7': {'ithaca': 1351, 'alltrails': 10017694}, 'Shindagin Hollow Y1': {'ithaca': 1352, 'alltrails': 10017694}, 'Shindagin Hollow Y2': {'ithaca': 1353, 'alltrails': 10017694}, 'Shindagin Hollow Y3': {'ithaca': 1354, 'alltrails': 10017694}, 'Shindagin Hollow Y4': {'ithaca': 1355, 'alltrails': 10017694}, 'Shindagin Hollow Y6': {'ithaca': 1356, 'alltrails': 10017694}, 'Shindagin Hollow Y7': {'ithaca': 1357, 'alltrails': 10017694}, 'Shindagin Hollow Y8': {'ithaca': 1358, 'alltrails': 10017694}, 'Shindagin Hollow Y9': {'ithaca': 1359, 'alltrails': 10017694}, 'Shindagin Hollow B1': {'ithaca': 1360, 'alltrails': 10017694}, 'Shindagin Hollow B2': {'ithaca': 1361, 'alltrails': 10017694}, 'Shindagin Hollow B3': {'ithaca': 1362, 'alltrails': 10017694}, 'Shindagin Hollow B4': {'ithaca': 1363, 'alltrails': 10017694}, 'Shindagin Hollow B5': {'ithaca': 1364, 'alltrails': 10017694}, 'Shindagin Hollow B6': {'ithaca': 1365, 'alltrails': 10017694}, 'Shindagin Hollow B7': {'ithaca': 1366, 'alltrails': 10017694}, 'Shindagin Hollow B9': {'ithaca': 1367, 'alltrails': 10017694}, 'Shindagin Hollow Entrance': {'ithaca': 1368, 'alltrails': 10017694}, 'Shindagin Hollow G1': {'ithaca': 1369, 'alltrails': 10017694}, 'Shindagin Hollow C2': {'ithaca': 1370, 'alltrails': 10017694}, 'Shindagin Hollow Y3 EXTENSION': {'ithaca': 1371, 'alltrails': 10017694}, 'Finger Lakes Trail - Shindagin Hollow FLT': {'ithaca': 1372, 'alltrails': 10017694}, 'Shindagin Hollow Y5': {'ithaca': 1373, 'alltrails': 10017694}, 'Six Mile Creek Natural Area': {'ithaca': 1382, 'alltrails': 10030675}, 'Cayuga Waterfront Trail (Stewart Park)': {'ithaca': 1379, 'alltrails': 10595923}, 'Ithaca Falls': {'ithaca': 1388, 'alltrails': 10032394}, 'Stewart Park': {'ithaca': 1389, 'alltrails': 10042562}, 'Cayuga Waterfront Trail': {'ithaca': 1390, 'alltrails': 10595923}, 'Sixmile Creek Walk': {'ithaca': 1393, 'alltrails': 10030675}}

def scrape_trail(section, id):
    trail = {}
    trail['Ithacatrails ID'] = id
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
    trails = {}
    names = set()
    for id in range(TRAIL_ID_INTERVAL[0], TRAIL_ID_INTERVAL[1]):
        print(id)
        trail_url = START_URL + str(id)
        r = requests.get(trail_url)
        soup = BeautifulSoup(r.content, "html5lib")
        section = soup.find(True, {"class": "trail-info two-thirds column"})
        if section:
            name = section.find('h1').get_text()
            if name not in names:
                names.add(name)
                trails[name] = scrape_trail(section, id)

    with open('alltrails_reviews.json') as json_file:
        alltrails_reviews = json.load(json_file)
        trails2 = {}
        for name in NAMES_WITH_BOTH_ID:
            ithaca_trail = trails[name]
            ithaca_trail['AllTrails ID'] = NAMES_WITH_BOTH_ID[name]['alltrails']
            ithaca_trail['Reviews'] = alltrails_reviews[str(ithaca_trail['AllTrails ID'])]
            trails2[name] = ithaca_trail
        with open('ithacatrails.json', 'w') as fout:
            json.dump(trails2 , fout, indent=4)
        print(trails2['Ellis Hollow Yellow trail'])
        return trails2

def get_trail_names():
    names = {}
    for id in range(TRAIL_ID_INTERVAL[0],TRAIL_ID_INTERVAL[1]):
        trail_url= START_URL + str(id)
        r = requests.get(trail_url)
        soup = BeautifulSoup(r.content, "html5lib")
        section = soup.find(True, {"class": "trail-info two-thirds column"})
        if section:
            names[section.find('h1').get_text()] = id
    print(len(names))
    return names

def names_with_both_ids():
    names_ithaca_id = get_trail_names()
    names_with_ids = {}
    for name in names_ithaca_id:
        if NAME_TO_ID[name] != None:
            names_with_ids[name] = {'ithaca': names_ithaca_id[name],
                                'alltrails': NAME_TO_ID[name]}
    return names_with_ids

scrape_all_trails()
# print(names_with_both_ids())

# print(len(NAMES_WITH_BOTH_ID))