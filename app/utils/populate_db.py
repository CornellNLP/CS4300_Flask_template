import json
import time
import os
import sys
import pickle

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

# some_engine = create_engine('postgresql://postgres:alpine@35.188.248.54:5432/learnddit')

# # create a configured "Session" class
# Session = sessionmaker(bind=some_engine)

# # create a Session
# session = Session()
# session.rollback()
comment_counter = 0
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
      objs = json.loads(line)
      count = len(objs)
      # iterate through all the comments of this
      for obj in objs:
        counter+=1
        upvotes = obj["ups"] if "ups" in obj else 0
        comment = Comment(obj["id"], obj["author"], obj["subreddit"], obj["link_id"], obj["body"], obj["score"], obj["gilded"], upvotes, obj["controversiality"])
        try:
          db.session.add(comment)
          db.session.commit()
        except Exception as e:
          db.session.rollback()
          print counter
          continue
        if counter % 3000 == 0:
          print "", float(counter)/count, "%\r"
  print "completed", filename
end_time = int(time.time())
print comment_counter, "comments"
print "finished in", (end_time-start_time)

f = open(os.path.dirname(os.path.abspath(__file__)) + "/filenames_db.pkl","wb")
pickle.dump(files,f)
f.close()