import praw
import json

reddit = praw.Reddit(user_agent='comment_query', client_id='WsGOFsPaaGtYVQ', client_secret="qPogCXpTh1wZylbQqES6JY04PVw")

comment = reddit.comment(id="d65la39")

comment_json = {}
comment_json["body"] = str(comment.body.encode('utf-8'))
comment_json["author"] = str(comment.author)
comment_json["score"] = comment.score
comment_json["ups"] = comment.ups
comment_json["downs"] = comment.downs
comment_json["subreddit"] = comment.subreddit_name_prefixed
comment_json["permalink"] = comment.permalink
comment_json["gilded"] = comment.gilded

js = json.dumps(comment_json)

print js