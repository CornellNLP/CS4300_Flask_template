import requests
from bs4 import BeautifulSoup
import json

# def get_headers(url):
#     page = requests.get(url)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     return soup.find_all("span", "mw-headline")


def buildUrl(wiki):
    return "https://en.wikipedia.org" + wiki


def writeToJson(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)
    return


def getAllCitiesTable():
    wiki_all_cities = "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"
    table_class = "wikitable"
    page = requests.get(wiki_all_cities)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_tables = soup.find_all('table', attrs={'class': table_class})
    return all_tables[1]


def getLinkAndCityName(tds):
    i = len(tds) - 10
    city_cell = tds[i]
    link = city_cell.find('a')
    url = buildUrl(link['href'])
    city_name = link['title']
    return url, city_name


def getPopulationAndPopDensity(tds):
    i = len(tds) - 10
    pop_cell = tds[i+2]
    pop = int(pop_cell.text.strip().replace(',', ''))
    pop_density_cell = tds[i+7]
    pop_density = int(pop_density_cell.text.strip().replace(
        '/sq\xa0mi', '').replace(',', ''))
    return pop, pop_density


def buildBasicDatasetStructure(sample=False):
    table = getAllCitiesTable()
    trs = table.find_all('tr')
    db = {}
    j = 10 if sample else len(trs)
    for tr in trs[1:j]:
        tds = tr.find_all('td')
        url, city_name = getLinkAndCityName(tds)
        pop, pop_density = getPopulationAndPopDensity(tds)
        db[url] = {"city_name": city_name, "population": pop,
                   "population_density": pop_density}
    return db


def clean(s):
    # todo: remove all the \u____ characters
    # remove all the citations [xx]
    return s.strip()


def getParagraphTextForUrl(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    main_text = soup.find('div', attrs={'id': 'mw-content-text'})
    pars = main_text.find_all('p')
    return [clean(p.text) for p in pars]


def addTextToDataset(db):
    for url, info in db.items():
        paragraphs = getParagraphTextForUrl(url)
        info["text"] = paragraphs
    return


db = buildBasicDatasetStructure(sample=True)
addTextToDataset(db)
writeToJson(db, "db.json")
