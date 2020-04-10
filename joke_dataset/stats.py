# run to update stats.txt with statistics on jokes
from glob import glob
import json
from pathlib import Path

cat_list = {} #dictionary w/ (key, value) = (category name, number of jokes in category)
source_list = {} #dictionary w/ (key, value) = (source, number of jokes from source)
total_jokes = 0 #total number of jokes in dataset

num_unclassified = 0 #total number of jokes that are unclassified
num_noscore = 0 #total number of jokes that do not have a score 

for filename in glob('./json/data_preprocess/*json'): #loop over .json files
    with open(filename) as f: 
        data = json.load(f) #open the json file 
        source_num = 0
        for obj in data:
            source_num = source_num + 1
            total_jokes += 1
            if len(obj['categories']) == 0:
                num_unclassified += 1
                continue

            if obj['score'] is None: 
                num_noscore +=1

            for cat in obj['categories']: 
                if cat not in cat_list.keys():
                    cat_list[cat] = 1
                else:
                    cat_list[cat] = cat_list[cat] +1
        source_list[filename] = source_num
        f.close()

cat_list = sorted(cat_list.items(), key=lambda item: item[0])
source_list = sorted(source_list.items(), key=lambda item: item[0])

f = open("stats.txt", "w+")

str1 = "Total Number of Jokes: " + str(total_jokes) + "\n"
f.write(str1)

f.write("\nNumber of jokes without categories: \n" + str(num_unclassified) + "\n")
f.write("\nCategories: \n")
for item in cat_list:
    s = item[0] + ": "+ str(item[1]) + " jokes \n"
    f.write(s)

f.write("\nNumber of jokes without scores: \n" +str(num_noscore) + "\n")
f.write("\nSources: \n")
for item in source_list:
    s = item[0] + ": " + str(item[1]) + " jokes \n"
    f.write(s)

f.close()