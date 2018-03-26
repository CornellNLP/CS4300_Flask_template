import json

rel_comments = []
subreddits = ["iwanttolearn"]
# subreddits = ["iwanttolearn", "explainlikeimfive", "socialskills", "lifeprotips", "improvementhub", "getdisciplined", "selfimprovement", "decidingtobebetter", "stopdrinking", "learnprogramming", "languagelearning", "confidence", "getmotivated", "everymanshouldknow", "youshouldknow", "askscience", "askhistorians", "coolguides"]

print "starting parser"
with open("RC_2017-02", "r") as file:
  print "file loaded!"
  print "-----------------"

  flag = True

  for comment in file:
    if flag:
      print "beginning to read lines..."
      flag = False
    obj = json.loads(comment)
    if obj["subreddit"].lower() in subreddits:
      if obj["body"] == "[removed]" or obj["body"] == "[deleted]" or obj["score"] < 0:
        continue
      print obj["body"]
      rel_comments.append(obj)



with open('data.json', 'w') as outfile:
    json.dump(rel_comments, outfile)