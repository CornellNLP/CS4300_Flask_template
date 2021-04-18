import json
import csv

with open('modzcta.json') as f:
    shapeData = json.load(f)

with open('final_data.csv', newline='') as f:
    reader = csv.reader(f, quotechar='|')
    covidList = list(reader)[1:] # remove header

# create dict
covidDict = {}
for d in covidList:
    covidDict[d[0]] = d[1:]

# find desired columns
columnDict = { 
    'lat': 0, 
    'lon': 1, 
    'people_tested': 2, 
    'people_positive': 3,
    '%_positive': 4, 
    '%_at_least_1': 5, 
    '%_full_vax': 6
}
columns = ['%_positive', '%_full_vax']

# Todo: filter for Manhattan
for geom in shapeData['features']:
    modzcta = geom['properties']['modzcta']
    if modzcta in covidDict:
        row = covidDict[modzcta]
        for c in columns:
            geom['properties'][c] = row[columnDict[c]]
    else:
        for c in columns:
            geom['properties'][c] = None

    
with open('shapeData.json', 'w') as outfile:
    json.dump(shapeData, outfile)