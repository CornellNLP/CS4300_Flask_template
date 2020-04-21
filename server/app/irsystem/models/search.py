from . import *
from bs4 import BeautifulSoup
from selenium import webdriver


# setup for getting the video url since its javascript and needs to load
# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# driver = webdriver.Chrome(options=options)


# test topics
topics = ['healthcare', 'terrorism', 'national security', 'gun policy', 'taxes',
          'education', 'economy', 'immigration', 'abortion', 'federal deficit',
          'climate change', 'environment', 'war', 'corona virus', 'covid 19']


# save video links so we don't have to requery
videos = dict()


def exact_search(transcript, topic, candidates):
    return [x for x in transcript if topic in x['text'] and (x['speaker'] in candidates or len(candidates) == 0)]


def search(topics, candidates, debate_name):
    debate = debates.find_one({'title': debate_name})

    relevant = []
    for topic in topics:
        for part in debate['parts']:
            for x in exact_search(part['text'], topic, candidates):
                relevant.append((part['video'], x))

    relevant_transformed = []
    for video_link, quote in relevant:
        if video_link not in videos:
            videos[video_link] = video_link

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
# def get_video_link(url):
#     # execute a webdriver request
#     driver.get(url)
#     video_page = BeautifulSoup(driver.page_source, 'html.parser')
#     return video_page.find('video').attrs['src']


# tags are:
# one of: "debate", "town hall", "speech", "interview",
# hierarchy (only one of which):
#                                                   [year] election
#                           [year] presidential election         etc
# [year] democratic presidential primary       [year] republican presidential primary   [year] presidential general election

