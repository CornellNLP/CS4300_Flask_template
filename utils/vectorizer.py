import json
import math
import string
import time
import os
import sys
import enchant
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer

path = sys.argv[1]

print "starting vectorization of words..."
start_time = int(time.time())

tokenizer = TreebankWordTokenizer()
stop_words = set(stopwords.words('english'))
d = enchant.Dict("en_US")

inv_index = {}
for filename in os.listdir(os.getcwd() + "/" + path):
  if "json" not in filename:
    continue
  filename = path + "/" + filename
  with open(filename, "r") as file:
    print "starting", filename
    counter = 0
    for line in file:
      objs = json.loads(line)
      count = len(objs)

      # iterate through all the comments of this
      for obj in objs:
        # remove automoderator comments
        if obj["author"].encode("utf-8").lower() is "automoderator":
          continue
        comment_id = obj["id"]
        body = obj["body"].encode("utf-8")

        # bye bye punctuation
        body = body.lower().translate(None, string.punctuation)

        # tokenize comments
        for word in tokenizer.tokenize(body):
          # remove stop words and links
          if word in stop_words or "http" in word or "www" in word or not word:
            continue

          # place into inverted index
          if word in inv_index:
            if comment_id in inv_index[word]:
              inv_index[word][comment_id]+=1
            else:
              inv_index[word][comment_id]=1
          elif d.check(word):
            inv_index[word]={comment_id:1}
        counter+=1

        # print counter
        if counter % 3000 == 0:
          print "", float(counter)/count, "%\r"
  print "completed", filename
end_time = int(time.time())
print "finished in", (end_time-start_time)

f = open("inv_index.pkl","wb")
pickle.dump(inv_index,f)
f.close()
