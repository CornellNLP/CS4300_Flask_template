import json
import time
import sys

subreddits = ["iwanttolearn", "explainlikeimfive"]
filename = sys.argv[1]

print "starting parser"
start_time = int(time.time())

rel_comments = 0
counter = 0
with open(filename, "r") as file:
  with open(filename + ".json", 'w') as outfile:
    print "file loaded!"
    print "-----------------"

    flag = True

    for comment in file:
      counter+=1
      if flag:
        print "beginning to read lines..."
        epoch_time = int(time.time())

        flag = False
      obj = json.loads(comment)
      if obj["subreddit"].lower() in subreddits:
        if obj["body"] == "[removed]" or obj["body"] == "[deleted]" or obj["score"] < 0:
          continue
        rel_comments+=1
        outfile.write(json.dumps(obj))

end_time = int(time.time())
print "Took", (end_time - start_time), "seconds to parse", counter, "comments."
print "Resulting list has", len(rel_comments), "comments"