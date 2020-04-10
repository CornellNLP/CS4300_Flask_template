import re
import sys
from collections import defaultdict

import requests
from bs4 import BeautifulSoup


# execute a request, if it fails then print and exit, other return souped text
def get_bs_request(url):
    request_response = requests.get(url)
    if not request_response.ok:
        print(request_response)
        sys.exit()
    return BeautifulSoup(request_response.text, 'html.parser')


def tokenize(text):
    """Returns a list of words that make up the text.

    Note: for simplicity, lowercase everything.
    Requirement: Use Regex to satisfy this function

    Params: {text: String}
    Returns: List
    """

    return re.findall(r'[a-z]+', text.lower())


# debate link
debate_link = 'https://www.rev.com/blog/transcripts/south-carolina-democratic-debate-transcript-february-democratic-debate'
soup = get_bs_request(debate_link)

# get each response
transcript_text = soup.find('div', class_='fl-callout-text').find_all('p')
transcript_text = [q for q in transcript_text if len(q.contents) == 5]
speaker_text = []
for quote in transcript_text:
    name = quote.contents[0].split(':')[0].strip()
    time = quote.contents[1].text
    text = quote.contents[4]
    speaker_text.append((name, time, text))


speakers1 = defaultdict(int)
for s in speaker_text:
    speakers1[s[0]] += 1
print('Times spoken per speaker: ')
print(speakers1)


tokenized_text = []
tokens = set()
for s in speaker_text:
    ts = tokenize(s[2])
    tokenized_text.append((s[0], s[1], ts))
    for t in ts:
        tokens.add(t)
print('\nNumber of unique tokens: ' + str(len(tokens)))


speakers2 = defaultdict(int)
for s in tokenized_text:
    speakers2[s[0]] += len(s[2])
print('\nTokens per speaker: ')
print(speakers2)


speaker_tokens = dict()
for s in tokenized_text:
    if s[0] not in speaker_tokens:
        speaker_tokens[s[0]] = defaultdict(int)
    for w in s[2]:
        speaker_tokens[s[0]][w] += 1
print('\nSpeaker\'s top tokens: ')
for k, v in speaker_tokens.items():
    print(k)
    print(sorted(v.items(), key=lambda x: x[1], reverse=True)[:10])


all_tokens = defaultdict(int)
for _, v in speaker_tokens.items():
    for k, val in v.items():
        all_tokens[k] += val
print('\nOverall top tokens: ')
print(sorted(all_tokens.items(), key=lambda x: x[1], reverse=True)[:10])
