import re

import requests
from bs4 import BeautifulSoup

from . import *


# test topics
topics = ['healthcare', 'terrorism', 'national security', 'gun policy', 'taxes',
          'education', 'economy', 'immigration', 'abortion', 'federal deficit',
          'climate change', 'environment', 'war', 'corona virus', 'covid 19']


# save video links so we don't have to requery
# TODO: this should go in a database
videos = dict()


def exact_search(transcript, topic):
    return [x for x in transcript if topic in x['text']]


def search(topics, candidates, debate_name):
    debate = debates.find_one({'title': debate_name})

    relevant = []
    for topic in topics:
        for part in debate['parts']:
            for x in exact_search(part['text'], topic):
                relevant.append((part['video'], x))

    relevant_transformed = []
    for video_link, quote in relevant:
        if video_link not in videos or videos[video_link] is None:
            videos[video_link] = get_video_link(video_link)

        relevant_transformed.append({
            "video": videos[video_link],
            "quotes": [{
                "speaker": quote['speaker'],
                "candidate": quote['speaker'] in debate['candidates'],
                "question": quote['question'],
                "time": quote['time'],
                "text": quote['text']
            }]
        })

    return [{
        "title": debate['title'],
        "date": debate['date'],
        "description": debate['description'],
        "results": relevant_transformed
    }]


# as the link is only good for a day, this must be done on demand
def get_video_link(url):
    request_response = requests.get(url)
    if request_response.ok:
        pattern = re.compile('(?<="mediaUrl":").+?(?=")')

        soup = BeautifulSoup(request_response.text, 'html.parser')
        script = soup.find('script', text=pattern)
        if script:
            match = pattern.search(str(script))
            if match:
                return match.group(0)
    return None


# tags are:
# one of: "debate", "town hall", "speech", "interview",
# hierarchy (only one of which):
#                                                   [year] election
#                           [year] presidential election         etc
# [year] democratic presidential primary       [year] republican presidential primary   [year] presidential general election

