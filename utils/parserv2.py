import json
import time
import sys

subreddits = ["iwanttolearn", "explainlikeimfive"]
filename = sys.argv[1]

print "starting parser"
start_time = int(time.time())

rel_comments = []
counter = 0

with open(filename, "r") as file:
  print "file loaded!"
  print "-----------------"

  flag = True

  for comment in file:
    counter+=1
    if flag:
      print "beginning to read lines..."

      flag = False
    obj = json.loads(comment)
    if obj["subreddit"].lower() in subreddits:
      if obj["body"] == "[removed]" or obj["body"] == "[deleted]" or obj["score"] < 0:
        continue
      rel_comments.append(json.dumps(obj))

with open(filename + ".json", 'w') as outfile:
  json.dump(rel_comments, outfile)
end_time = int(time.time())
print "Took", (end_time - start_time), "seconds to parse", counter, "comments."
print "Resulting list has", len(rel_comments), "comments"