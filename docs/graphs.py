import numpy as np
import json
from collections import Counter
import matplotlib.pyplot as plt

with open("data.json", 'r') as f:
    datastore = json.load(f)

parent_ids = [comment['parent_id'] for comment in datastore]

id_counts = Counter(parent_ids)
# print(id_counts.values())
num_comm_counts = Counter(id_counts.values())

x, y = zip(*[(x, y) for (x,y) in num_comm_counts.items()])

# print(num_comm_counts)
plt.bar(x, y)
plt.yscale('log')
plt.xlabel('# Comments on Post')
plt.ylabel('# Posts')
plt.title('# Posts vs # Comments on Post')
plt.show()