import json
from nltk.tokenize import word_tokenize


def get_debate(filename):
    with open(filename) as f:
        return json.load(f)


def fix_addressing(debate):
    speakers = eval(debate['candidates']).union(eval(debate['moderators']))
    speakers_dict = dict()
    for name in speakers:
        for name_part in name.lower().split(' '):
            if name_part in speakers_dict:
                speakers_dict[name_part] = None
            else:
                speakers_dict[name_part] = name
    # remove names that can point to multiple people
    speakers_dict = {k: v for k, v in speakers_dict.items() if v is not None}

    for i, line in enumerate(debate['speaker_text']):
        if line[0] not in speakers:
            name = None
            for name_part in line[0].lower().split(' '):
                if name_part in speakers_dict:
                    name = speakers_dict[name_part]
                    break
            if name is None:
                raise Exception('Name ' + line[0] + ' cannot be matched')
            line[0] = name

    return speakers_dict, debate


def combine_speakers(transcript):
    new_transcript = [{'speaker': None}]
    for x in transcript:
        if x[0] == new_transcript[-1]['speaker']:
            # new_transcript[-1]['text'] += ' ' + x['text'].strip()
            new_transcript[-1]['text'] += ' ' + x[2].strip()
        else:
            # new_transcript.append(x)
            new_transcript.append({'speaker': x[0], 'time': x[1], 'text': x[2].strip()})
    return new_transcript[1:]


def exact_search(transcript, topic):
    return [x for x in transcript if topic in x[2]]


debate = get_debate('output/december-democratic-debate-transcript-sixth-debate-from-los-angeles.txt')
speakers_dict, debate = fix_addressing(debate)
transcript = combine_speakers(debate['speaker_text'])

candidates = eval(debate['candidates'])
moderators = eval(debate['moderators'])
for i, line in enumerate(transcript):
    if line['speaker'] in moderators:
        line['question'] = '?' in line['text']
        if line['question']:
            r = []
            for x in word_tokenize(line['text'].lower().replace('-', '')):
                if x in speakers_dict:
                    r.append(speakers_dict[x])
            if r:
                line['addressed_to'] = r[-1]
            else:
                print()
    else:
        if 'question' and transcript[i-1]['question']:
            if 'addressed_to' in transcript[i-1] and line['speaker'] == transcript[i-1]['addressed_to']:
                line['response_to'] = i-1
            else:
                print()




topics = ['healthcare', 'terrorism', 'national security', 'gun policy', 'taxes',
          'education', 'economy', 'immigration', 'abortion', 'federal deficit',
          'climate change', 'environment', 'war', 'corona virus', 'covid 19']

# for topic in topics:
#     print(topic)
#     for x in exact_search(transcript, topic):
#         print(x)
#     print()
