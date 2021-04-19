import numpy as np
import pandas as pd
print("fuck")


#kaggle_file = '../datasets/kaggle_data.csv'
#df = pd.read_csv(kaggle_file, na_values='')


def test():
    name = 'transcripts/Avatar The Last Airbender/avatar_scripts_s1_e1.txt'
    file = open(name)
    fileContents = file.read()
    file.close()
    # print(fileContents)

    start = fileContents.index('Print')
    end = fileContents.rfind("Transcripts")
    return fileContents[start+5: end]


print(test())
