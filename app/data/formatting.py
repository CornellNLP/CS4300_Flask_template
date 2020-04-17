import json
import os


def generate_speakers_dict(debate):
    speakers = set(debate['candidates'] + debate['other_speakers'])
    speakers_dict = dict()
    for name in speakers:
        for name_part in name.lower().split(' '):
            if name_part in speakers_dict:
                speakers_dict[name_part] = None
            else:
                speakers_dict[name_part] = name

    # remove names that can point to multiple people
    return {k: v for k, v in speakers_dict.items() if v is not None}


def fix_addressing(debate, speakers_dict):
    speakers = set(debate['candidates'] + debate['other_speakers'])
    for part in debate['parts']:
        for line in part['text']:
            if line['speaker'] not in speakers:
                name = None
                for name_part in line['speaker'].lower().split(' '):
                    if name_part in speakers_dict:
                        name = speakers_dict[name_part]
                        break
                if name is None:
                    raise Exception('Name ' + line['speaker'] + ' cannot be matched')
                line['speaker'] = name

    return speakers_dict, debate


# TODO: fix unicode


def annotate_questions(debate):
    other_speakers = set(debate['other_speakers'])
    for part in debate['parts']:
        for i, line in enumerate(part['text']):
            line['question'] = line['speaker'] in other_speakers and ('?' in line['text'] or len(line['text']) > 150)


def combine_speakers(debate):
    for i, part in enumerate(debate['parts']):
        new_transcript = [{'speaker': None}]
        for line in part['text']:
            if line['speaker'] == new_transcript[-1]['speaker']:
                new_transcript[-1]['text'] += ' ' + line['text']
            else:
                new_transcript.append(line)
        debate['parts'][i]['text'] = new_transcript[1:]


def combine_speakers_interrupting(debate):
    candidates = set(debate['candidates'])
    for i, part in enumerate(debate['parts']):
        new_transcript = [{'speaker': None}, {'speaker': None}]
        for line in part['text']:
            # candidate continuing to speak
            a = line['speaker'] == new_transcript[-2]['speaker'] and line['speaker'] in candidates and len(new_transcript[-2]['text']) > 150
            # not missing anything important
            b = a and not new_transcript[-1]['question'] and len(new_transcript[-1]['text']) < 75
            if b:
                # someone tries to interrupt, but candidate keeps going
                new_transcript.pop()
                new_transcript[-1]['text'] += ' ' + line['text']
                new_transcript[-1]['question'] = new_transcript[-1]['question'] or line['question']
                continue
            else:
                new_transcript.append(line)
        debate['parts'][i]['text'] = new_transcript[2:]


def annotate_responses(debate):
    candidates = set(debate['candidates'])
    other_speakers = set(debate['other_speakers'])
    for part in debate['parts']:
        for i, line in enumerate(part['text']):
            if line['speaker'] in candidates and not line['question']:
                # check if responding to another candidate
                if part['text'][i-1]['speaker'] in candidates and len(part['text'][i-1]['text']) > 50:
                    line['response'] = i-1
                # TODO: if respond or response in moderators' question then link and use names?
                else:
                    # find the last question asked
                    for x in range(i-1, -1, -1):
                        if part['text'][x]['question']:
                            line['response'] = x
                            part['text'][x]['response'].append(i)
                            break

                if 'response' not in line:
                    # find the last other speaker
                    for x in range(i-1, -1, -1):
                        if part['text'][i-1]['speaker'] in other_speakers:
                            line['response'] = x
                            part['text'][x]['response'].append(i)
                            break

                if 'response' not in line:
                    line['response'] = i - 1

            else:
                line['response'] = []


url = 'debates/december-democratic-debate-transcript-sixth-debate-from-los-angeles.txt'
with open(url) as f:
    debate = json.load(f)

speakers_dict = generate_speakers_dict(debate)
combine_speakers(debate)
annotate_questions(debate)
combine_speakers_interrupting(debate)
annotate_responses(debate)

text = debate['parts'][0]['text'] + debate['parts'][1]['text'] + debate['parts'][2]['text']
# [x for x in text if type(x['response']) == list and len(x['response']) > 3]

for part in debate['parts']:
    for i, line in enumerate(part['text']):
        print(i)
        print(line['speaker'])
        print(line['text'])
        print(line['question'])
        print(line['response'])
        print('---')


# folder = 'debates/'
# for file_name in os.listdir(folder):
#     with open(folder + file_name) as f:
#         debate = json.load(f)
#
#     # a dictionary mapping partial names to the full names
#     speakers_dict = generate_speakers_dict(debate)
#
#     # add whether they are questions
#     annotate_questions(debate)
#
#     # combining same speaker blocks together
#     combine_speakers(debate)
#
#     # correct all text speakers to match the candidates/ other_speakers fields
#     fix_addressing(debate, speakers_dict)
#
#     # link questions and responses together
#     annotate_responses(debate, speakers_dict)
#
#     with open(folder + file_name, 'w') as f:
#         f.write(json.dumps(debate, default=str))
