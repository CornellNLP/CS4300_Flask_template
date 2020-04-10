import re
import sys
import nltk
from collections import defaultdict
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
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


def build_inverted_index(msgs):
    output_dict = {} 
    
    for i in range(len(msgs)): 
        msg = msgs[i]
        tokens = msg['toks']
        
        for token in set(tokens): 
            count = tokens.count(token)
            tup = (i,  count)
            
            if token in output_dict.keys():
                output_dict[token].append(tup)
            else: 
                output_dict[token] = []
                output_dict[token].append(tup)
        
    return output_dict

def boolean_and_search(word1, word2, inverted_index): 
    if word1 in inverted_index and word2 in inverted_index: 
        list_1 = inverted_index[word1]
        list_2 = inverted_index[word2]
    else:
        return []

    output_list = []

    i = 0 
    j = 0 

    while i < len(list_1) and j < len(list_2):
        if list_1[i][0] == list_2[j][0]: 
            output_list.append(list_1[i][0])
            i +=1
            j +=1
        else: 
            if list_1[i][0] < list_2[j][0]: 
                i+=1
            else: 
                j+=1
    
    return output_list

def convert_to_seconds(input_string): 
    m,s = input_string.split(':')
    total_seconds = int(m) * 60 + int(s)
    return total_seconds 



# debate link
debate_link = 'https://www.rev.com/blog/transcripts/south-carolina-democratic-debate-transcript-february-democratic-debate'
soup = get_bs_request(debate_link)

# get each response
transcript_text = soup.find('div', class_='fl-callout-text').find_all('p')
transcript_text = [q for q in transcript_text if len(q.contents) == 5]

stop_words=set(stopwords.words('english'))


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
    ts = list(filter(lambda w: not w in stop_words,tokenize(s[2])))
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


flat_msgs = []
add_time = 0
old_time = 0

for s in speaker_text: 
    msg = dict()
    msg['speaker'] = s[0]
    new_time = convert_to_seconds(s[1])
    if new_time < old_time: 
        add_time += old_time 
    msg['time_stamp'] = new_time + add_time
    old_time = new_time
    msg['toks'] = list(filter(lambda w: not w in stop_words,tokenize(s[2])))
    flat_msgs.append(msg)

inv_idx = build_inverted_index(flat_msgs)


def show_word_freq(word, inv_idx): 
    search = inv_idx[word]

    x = []
    for i in search: 
        x.append(flat_msgs[i[0]]['time_stamp'])

    max_x = flat_msgs[-1]['time_stamp']

    plt.hist(x, range=(0,max_x))
    plt.ylim(top=len(search))
    plt.show()

#show_word_freq('climate', inv_idx)
