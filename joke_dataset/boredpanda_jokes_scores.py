import json
import matplotlib.pyplot as plt

def get_score_buckets():
    data = None
    result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    with open('./json/boredpanda_jokes.json') as f:
        data = json.load(f)

    for obj in data:
        scr = obj['score']
        idx = int(scr / 5)
        result[idx] += 1

    return result

def graphit(y):
    x = ['0-5', '5-10', '10-15', '15-20', '20-25', '25-30', '30-35', '35-40', '40-45', '45-50', '50-55', '55-60', '60-65', '65-70']
    plt.bar(x,y)

    plt.xlabel('range of upvotes')
    plt.ylabel('number of jokes')

    for index, value in enumerate(y):
        plt.text(index, value, str(value))

    plt.title('Winice <3 (boredpanda_jokes)')
    plt.show()

y_axis = get_score_buckets()
print(y_axis)
graphit(y_axis)
