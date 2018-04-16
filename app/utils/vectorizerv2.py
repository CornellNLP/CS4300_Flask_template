# import json
# import math
# import string
# import time
# import os
# import sys
# import enchant
# import pickle
# import nltk
# import re
# from nltk.corpus import stopwords
# from nltk.tokenize import TreebankWordTokenizer

# '''
# This file will parse each word into its individual vocabulary while keeping track of words that are used, in order to minimize memory being used at any given time
# '''

# saved_path = "data/"

# path = sys.argv[1]

# print "starting vectorization of words..."
# start_time = int(time.time())

# tokenizer = TreebankWordTokenizer()
# stop_words = set(stopwords.words('english'))
# d = enchant.Dict("en_US")

# f = open("words_v2.pkl","rb")
# words = pickle.load(f);

# f = open("filenames_v2.pkl","rb")
# files = pickle.load(f)

# words = set([])
# files = set([])

# numbers = re.compile("^[0-9]{1,45}$")

# for filename in os.listdir(os.getcwd() + "/" + path):
#   if "json" not in filename:
#     continue

#   if filename in files:
#     print filename, "already processed!"
#     continue

#   files.add(filename)
#   filename = path + "/" + filename
#   with open(filename, "r") as file:
#     print "starting", filename
#     counter = 0
#     for line in file:
#       objs = json.loads(line)
#       count = len(objs)

#       # iterate through all the comments of this
#       for obj in objs:
#         # remove automoderator comments
#         if obj["author"].encode("utf-8").lower() is "automoderator":
#           continue
#         comment_id = obj["id"]
#         body = obj["body"].encode("utf-8")

#         # bye bye punctuation
#         body = body.lower().translate(None, string.punctuation)

#         # tokenize comments
#         for word in tokenizer.tokenize(body):
#           # remove stop words and links
#           if word in stop_words or "http" in word or "www" in word or not word:
#             continue
#           if numbers.match(word):
#             continue
#           # place into inverted index
#           if word in words:
#             # load word pkl file
#             f = open(saved_path + word + ".pkl","rb")
#             word_dict = pickle.load(f)
#             f.close()
#             if comment_id in word_dict:
#               word_dict[comment_id]+=1
#             else:
#               word_dict[comment_id]=1
#             f = open(saved_path + word + ".pkl","wb")
#             pickle.dump(word_dict,f)
#             f.close()
#           elif d.check(word):
#             word_dict = {comment_id: 1}
#             words.add(word)
#             f = open(saved_path + word + ".pkl","wb")
#             pickle.dump(word_dict, f)
#             f.close()
#         counter+=1

#         # print counter
#         if counter % 3000 == 0:
#           print "", float(counter)/count, "%\r"
#   print "completed", filename
# end_time = int(time.time())
# print "finished in", (end_time-start_time)

# f = open("filenames_v2.pkl","wb")
# pickle.dump(files,f)
# f.close()

# f = open("words_v2.pkl","wb")
# pickle.dump(words,f)
# f.close()
