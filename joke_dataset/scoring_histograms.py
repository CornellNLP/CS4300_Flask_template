import json
import matplotlib.pyplot as plt

def createScoreHistogram(data):
    plt.hist(data, density=False, bins = 5)  # `density=False` displays counts, #change number of bins for num of bins on histogram
    plt.xlim(0, 5) #change limit of x axis (score)
    plt.ylabel('Number')
    plt.xlabel('Score')
    plt.show()

string = ############## ENTER JSON FILE PATH YOU WANT TO CREATE HISTOGRAM OF ###############
with open(string) as f:
    data = json.load(f)
    scores = [obj['score'] for obj in data]
    createScoreHistogram(scores)
    f.close()
    