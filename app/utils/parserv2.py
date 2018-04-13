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
      # eliminates short replies
      short_reply = "t1" in obj["parent_id"] and len(obj["body"]) < 30

      # elimintes thanks!
      is_thanks_reply = "t1" in obj["parent_id"] and "thank" in obj["body"].lower()

      # eliminates removed comments
      is_deleted = obj["body"] == "[removed]" or obj["body"] == "[deleted]"

      # eliminates poor scoring comments
      downvoted = obj["score"] < 0

      # eliminates most useless ELI5 comments
      bad_eli5 = obj["score"] <= 1 and obj["subreddit"].lower() == "explainlikeimfive"

      # eliminates automoderator comments
      is_automod = obj["author"].lower() == "automoderator"

      bad_comment = short_reply or is_deleted or downvoted or bad_eli5 or is_automod
      if bad_comment:
        continue
      rel_comments.append(obj)

end_time = int(time.time())
print "Took", (end_time - start_time), "seconds to parse", counter, "comments."
print "Initial resulting list has", len(rel_comments), "comments"

max_depth = 4
rel_tree = {}
filtered_comments = []

print "Trimming comments past depth", max_depth
start_time = int(time.time())

# get all top level comments
for comment in rel_comments:
  if "t3" in comment["parent_id"]:
    rel_tree[comment["id"]] = 0
    rel_comments.remove(comment)
    filtered_comments.append(comment)

print "finished finding parent comments"

for i in range(max_depth):
  for comment in rel_comments:
    if comment["parent_id"] in rel_tree:
      rel_tree[rel_tree[comment["id"]]] = comment["parent_id"]+1
      rel_comments.remove(comment)
      filtered_comments.append(comment)
  print "finished iteration", i

end_time = int(time.time())
print "Took", (end_time - start_time), "seconds to filter by depth"

with open(filename + ".json", 'w') as outfile:
  json.dump(filtered_comments, outfile)

print "Final resulting list has", len(filtered_comments), "comments"
