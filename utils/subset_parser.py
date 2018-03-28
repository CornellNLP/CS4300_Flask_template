import json
import time
import sys

subreddits = ["iwanttolearn", "explainlikeimfive"]
filename = sys.argv[1]

print "starting parser on subset of data"


max_depth = 4
rel_tree = {}
filtered_comments = []


rel_comments = []
counter = 0
with open(filename, "r") as file:
  with open(filename + "10mb.json", 'w') as outfile:
    for line in file:
      objs = json.loads(line)

      for obj in objs:
        obj = json.loads(obj)
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
        bad_comment = short_reply or is_deleted or downvoted
        if bad_comment:
          continue
        rel_comments.append(obj)

      objs = rel_comments

      for comment in objs:
        if "t3" in comment["parent_id"]:
          rel_tree[comment["id"]] = 0
          objs.remove(comment)
          filtered_comments.append(comment)
      print "finished parents"

      for i in range(max_depth):
        print "finished iteration", i
        for comment in objs:
          if comment["parent_id"] in rel_tree:
            rel_tree[rel_tree[comment["id"]]] = comment["parent_id"]+1
            objs.remove(comment)
            filtered_comments.append(comment)
      json.dump(filtered_comments, outfile)

