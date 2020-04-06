from glob import glob
import json

cat_list = {}
source_list = {}
num = 0
for filename in glob('./json/*.json'): #loop over .json files
    with open(filename) as f: 
        data = json.load(f) #open the json file 
        source_num = 0
        for obj in data:
            source_num = source_num + 1
            num = num + 1
            for cat in obj['categories']: 
                if cat not in cat_list.keys():
                    cat_list[cat] = 1
                else:
                    cat_list[cat] = cat_list[cat] +1
        source_list[filename] = source_num
        f.close()

f = open("JokeStats.txt", "w+")
str1 = "Number of Jokes:" + str(num) + "\n"
f.write(str1)
f.write("\nCategories: \n")
for item in cat_list.items():
    str2 = item[0] + ": "+ str(item[1]) + " jokes \n"
    f.write(str2)

f.write("\nSources: \n")
for item in source_list.items():
    str2 = item[0] + ": " + str(item[1]) + " jokes \n"
    f.write(str2)
f.close()

