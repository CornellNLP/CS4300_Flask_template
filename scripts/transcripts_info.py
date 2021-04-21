
import json
import os

with open('./datasets/final/tv_shows_to_index.json') as json_file:
  tv_shows_to_index = json.load(json_file)
  tv_shows = list(tv_shows_to_index.keys())

with open('./datasets/final/merged_tv_shows.json') as json_file_tv_info:
  tv_shows_info = json.load(json_file_tv_info)

streaming_platforms_missing_transcripts = {}
tv_shows_w_transcripts = []
tv_shows_no_transcripts = []
for show in os.listdir("./transcripts"):
  if show != ".DS_Store":
    tv_shows_w_transcripts.append(show.lower())

for show in os.listdir("./transcripts2"):
  if show != ".DS_Store":
    tv_shows_w_transcripts.append(show.lower())

for show in tv_shows:
  if not show.lower() in tv_shows_w_transcripts:
    tv_shows_no_transcripts.append(show)

# for show in tv_shows_no_transcripts:
#   for tv_show_info in tv_shows_info:
#       if tv_show_info['show_title'] == show:
#         streaming_platforms = tv_show_info['show_info']['streaming platform']
#         for streaming_platform in streaming_platforms:
#           if streaming_platform in streaming_platforms_missing_transcripts:
#             streaming_platforms_missing_transcripts[streaming_platform].append(show)
#           else:
#             streaming_platforms_missing_transcripts[streaming_platform] = [show]

print("There are transcripts for " + str(len(tv_shows_w_transcripts)) + " shows. " + str(len(tv_shows_no_transcripts)) + " shows are missing transcripts. ")
# print("These shows from Netflix are missing transcipts: " + str(streaming_platforms_missing_transcripts["Netflix"]))