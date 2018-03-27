import json
import re
import math
import matplotlib.pyplot as plt

jsonObject = json.load(open('sample_data.json'))

count_dict = {}

num_docs = len(jsonObject)

count = 0

for obj in jsonObject:

  text = obj['body']
  if text == "[deleted]":
    continue
  #remove new line characters
  text = text.replace("\n", "")
  word_list = re.findall(r"[a-z]+", text.lower())
  num_words = len(word_list)
  if num_words in count_dict:
    count_dict[num_words] = count_dict[num_words] + 1
  else:
    count_dict[num_words] = 1
  print(str(count) + ": " + text)
  count = count + 1

print(count_dict)
print(count_dict.values())
counts = count_dict.values()
plt.hist(counts, bins = 50)
plt.xlabel("# Words in Comment")
plt.ylabel("# Comments")
plt.title("# Comments vs # Words in Comment")
plt.show()