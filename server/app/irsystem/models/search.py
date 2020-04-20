from . import *
from bs4 import BeautifulSoup
from selenium import webdriver


# test topics
topics = ['healthcare', 'terrorism', 'national security', 'gun policy', 'taxes',
          'education', 'economy', 'immigration', 'abortion', 'federal deficit',
          'climate change', 'environment', 'war', 'corona virus', 'covid 19']


def exact_search(transcript, topic):
    return set(x for x in transcript if topic in x['text'])


def search(topics, candidates, debate_name):
    debate = debates.find({'title': debate_name})

    relevant = set()
    for topic in topics:
        for part in debate['parts']:
            for x in exact_search(part['text'], topic):
                relevant = relevant.intersection(x)
    return relevant


# as the link is only good for a day, this must be done on demand
def get_video_link(url):
    # setup for getting the video url since its javascript and needs to load
    # only needs to run once so restructure
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)

    # execute a webdriver request
    driver.get(url)
    video_page = BeautifulSoup(driver.page_source, 'html.parser')
    return video_page.find('video').attrs['src']


# tags are:
# one of: "debate", "town hall", "speech", "interview",
# hierarchy (only one of which):
#                                                   [year] election
#                           [year] presidential election         etc
# [year] democratic presidential primary       [year] republican presidential primary   [year] presidential general election

