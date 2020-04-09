import json
import matplotlib.pyplot as plt

def get_score_buckets():
    data = None
    result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    with open('./json/boredpanda_puns.json') as f:
        data = json.load(f)

    for obj in data:
        scr = obj['score']
        idx = int(scr / 25)
        result[idx] += 1

    return result

def graphit(y):
    x = ['0-25', '25-50', '50-75', '75-100', '100-125', '125-150', '150-175', '175-200', '200-225', '225-250', '250-275', '275-300', '300-325', '325-350', '350-375']
    plt.bar(x,y)

    plt.xlabel('range of upvotes')
    plt.ylabel('number of jokes')

    for index, value in enumerate(y):
        plt.text(index, value, str(value))

    plt.title('Winice <3 (boredpanda_puns)')
    plt.show()

y_axis = get_score_buckets()
print(y_axis)
graphit(y_axis)
