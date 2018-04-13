import json
import time
import sys
import os
import pickle

'''
this will now parse ALL jsons and overwrite them
'''

subreddits = ["iwanttolearn", "explainlikeimfive"]

print "starting parser on subset of data"

max_depth = 4
rel_tree = {}

path = sys.argv[1]

counter = 0
for filename in os.listdir(os.getcwd() + "/" + path):
  if "json" not in filename:
    continue
  filename = path + "/" + filename
  with open(filename, "r") as file:
    print "starting", filename
    rel_comments = []
    filtered_comments = []

    for line in file:
      objs = json.loads(line)

      for obj in objs:
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

      objs = rel_comments
      filtered_comments = rel_comments
        # for comment in objs:
        #   if "t3" in comment["parent_id"]:
        #     rel_tree[comment["id"]] = 0
        #     objs.remove(comment)
        #     filtered_comments.append(comment)
        # print "finished parents"

        # for i in range(max_depth):
        #   print "finished iteration", i
        #   for comment in objs:
        #     if comment["parent_id"] in rel_tree:
        #       rel_tree[rel_tree[comment["id"]]] = comment["parent_id"]+1
        #       objs.remove(comment)
        #       filtered_comments.append(comment)

      with open(filename, 'w') as outfile:
        counter+= len(filtered_comments)
        json.dump(filtered_comments, outfile)

f = open("n_docs.pkl","wb")
pickle.dump(counter,f)
f.close()

