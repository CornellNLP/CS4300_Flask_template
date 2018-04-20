import json
import time
import os
import sys
import pickle

sys.path.append(os.getcwd())

from app import db
from app.irsystem.models.comment import Comment

'''
This file will upload all the comments to the db!!!!
run this from the project root directory
e.g. python utils/populate_db.py utils/Parsed\ JSONs/
'''

path = sys.argv[1]

filepath =  os.path.dirname(os.path.abspath(__file__))

# f = open(filepath + "/filenames_db.pkl","rb")
# files = pickle.load(f)

files = set([])

ids = set([])

print "starting population of db..."
start_time = int(time.time())

for filename in os.listdir(os.getcwd() + "/" + path):
  if "json" not in filename:
    continue

  if filename in files:
    print filename, "already processed!"
    continue

  files.add(filename)

  filename = path + "/" + filename
  with open(filename, "r") as file:
    counter = 0
    print "starting", filename
    for line in file:
      counter+=1
      objs = json.loads(line)
      count = len(objs)
      # iterate through all the comments of this
      for obj in objs:
        upvotes = obj["ups"] if "ups" in obj else 0
        comment = Comment(obj["id"], obj["author"], obj["subreddit"], obj["link_id"], obj["body"], obj["score"], obj["gilded"], upvotes, obj["controversiality"])
        try:
          db.session.add(comment)
          db.session.commit()
        except:
          continue
        if counter % 3000 == 0:
          print "", float(counter)/count, "%\r"
  print "completed", filename
end_time = int(time.time())
print comment_counter, "comments"
print len(ids), "ids"
print id_confl, "conflicts"
print id_set, "set conflicts"
print "finished in", (end_time-start_time)

f = open(os.path.dirname(os.path.abspath(__file__)) + "/filenames_db.pkl","wb")
pickle.dump(files,f)
f.close()