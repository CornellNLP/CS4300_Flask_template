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


# links for the search page
url_pt1 = 'https://www.rev.com/blog/transcript-category/debate-transcripts/page/'
url_pt2 = '?view=all'
page = 1

debate_links = []
debates = dict()

soup = get_bs_request(url_pt1 + str(page) + url_pt2)
debate_results = soup.find_all('div', class_='fl-post-columns-post')
# while there are results
while len(debate_results) > 0:
    for result in debate_results:
        # add links to the transcript to the list
        link = result.find('a').attrs['href']
        debate_links.append(link)

    page += 1
    soup = get_bs_request(url_pt1 + str(page) + url_pt2)
    debate_results = soup.find_all('div', class_='fl-post-columns-post')

# for each debate transcript link
for debate_link in debate_links:
    soup = get_bs_request(debate_link)
    # intro paragraph for background info
    intro_text = soup.find_all('div', class_='fl-rich-text')[1].text

    # get each response
    transcript_text = soup.find('div', class_='fl-callout-text').find_all('p')
    transcript_text = [q for q in transcript_text if len(q.contents) == 5]
    speaker_text = []
    for quote in transcript_text:
        name = quote.contents[0].split(':')[0].strip()
        time = quote.contents[1].text
        text = quote.contents[4]
        speaker_text.append((name, time, text))

    # determine who are the candidates from the background info
    speakers = set((s[0] for s in speaker_text))
    candidates = set(c for c in speakers if c in intro_text)
    moderators = speakers.difference(candidates)

    # attempt to get the date from the background paragraph
    try:
        date = dateutil.parser.parse(intro_text, fuzzy=True).date()
    except:
        date = None

    # assemble all of the info in a dictionary
    debates[debate_link] = {
        'date': date,
        'candidates': candidates,
        'moderators': moderators,
        'summary': intro_text,
        'speaker_text': speaker_text
    }
