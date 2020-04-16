import json
import sys

import dateutil.parser
import requests
from bs4 import BeautifulSoup


# execute a request, if it fails then print and exit, other return souped text
def get_bs_request(url):
    request_response = requests.get(url)
    if not request_response.ok:
        print(request_response)
        sys.exit()
    return BeautifulSoup(request_response.text, 'html.parser')


# get all debate urls from the provided url
def get_debates(url):
    page = 1
    debates = set()
    debate_results = get_bs_request(url + '/page/' + str(page) + '?view=all')
    debate_results = debate_results.find_all('div', class_='fl-post-columns-post')
    # while there are results
    while len(debate_results) > 0:
        for result in debate_results:
            # add the transcript urls to the list
            debates.add(result.find('a').attrs['href'])

        page += 1
        debate_results = get_bs_request(url + '/page/' + str(page) + '?view=all')
        debate_results = debate_results.find_all('div', class_='fl-post-columns-post')

    return debates


# urls for the search pages
election_2020_url = 'https://www.rev.com/blog/transcript-category/2020-election-transcripts'
debates_url = 'https://www.rev.com/blog/transcript-category/debate-transcripts'

debate_urls = get_debates(election_2020_url).union(get_debates(debates_url))
bad_debates = {'https://www.rev.com/blog/transcripts/transcript-of-the-kamala-harris-and-joe-biden-heated-exchange', 'https://www.rev.com/blog/transcripts/transcript-from-first-night-of-democratic-debates'}
debate_urls -= bad_debates

# for each debate transcript url
for debate_url in debate_urls:
    debate = get_bs_request(debate_url)

    # background info for the debate
    intro_text = debate.find_all('div', class_='fl-rich-text')[1].text.strip()
    title = debate.find('h1', class_='fl-heading').text.strip()
    # attempt to get the date from the background paragraph
    try:
        date = dateutil.parser.parse(intro_text, fuzzy=True, ignoretz=True).date()
    except ValueError:
        date = None

    # get each response
    parts = []
    number = 1
    speakers = set()
    transcript_text = debate.find('div', class_='fl-callout-text')
    for e in transcript_text.children:
        if e.name == 'p' and len(e.contents) == 5:
            # text
            name = e.contents[0].split(':')[0].strip()
            clock = e.contents[1].text
            text = e.contents[4].strip()

            if not parts:
                # hopefully this signals the debate is only one part
                parts.append({'number': None, 'video': None, 'text': []})
            if parts[-1]['video'] is None:
                # url for video is in the text, not the heading
                parts[-1]['video'] = e.contents[1].attrs['href'].rsplit('&', 1)[0]

            speakers.add(name)
            parts[-1]['text'].append({'speaker': name, 'time': clock, 'text': text})
        elif e.name == 'h2':
            # new part
            parts.append({'number': number, 'video': None, 'text': []})
            number += 1
        else:
            print(debate_url)
            print(e)
            print()

    # determine who are the candidates from the background info
    candidates = set(c for c in speakers if c in intro_text)
    other_speakers = speakers.difference(candidates)

    # assemble all of the info in a dictionary
    debate_info = {
        'url': debate_url,
        'title': title,
        'date': date,
        'candidates': list(candidates),
        'other_speakers': list(other_speakers),
        'description': intro_text,
        'parts': parts
    }

    with open('output/' + debate_url.split('/')[-1] + '.txt', 'w') as f:
        f.write(json.dumps(debate_info, default=str))
