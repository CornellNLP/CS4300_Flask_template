import json
import time
import os
import sys

sys.path.append(os.getcwd())

from app import db
from app.irsystem.models.comment import Comment

'''
This file will upload all the comments to the db!!!!
run this from the project root directory
e.g. python utils/populate_db.py utils/Parsed\ JSONs/
'''

path = sys.argv[1]

print "starting population of db..."
start_time = int(time.time())

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
        upvotes = if "ups" in obj then obj["ups"] else 0
        comment = Comment(obj["id"], obj["author"], obj["subreddit"], obj["link_id"], obj["body"], obj["score"], obj["gilded"], upvotes, obj["controversiality"])
        db.session.add(comment)
        db.session.commit()
        counter+=1

        # print counter
        if counter % 3000 == 0:
          print "", float(counter)/count, "%\r"
  print "completed", filename
end_time = int(time.time())
print "finished in", (end_time-start_time)
