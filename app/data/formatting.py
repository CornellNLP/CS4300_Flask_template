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


def combine_speakers(parts):
    new_parts = []
    for part in parts:
        new_transcript = [{'speaker': None}]
        for line in part['text']:
            # TODO: handle dashes or short breaks to combine
            if line['speaker'] == new_transcript[-1]['speaker']:
                new_transcript[-1]['text'] += ' ' + line['text']
            else:
                new_transcript.append(line)
        new_parts.append(new_transcript[1:])
    return new_parts


def annotate_question_response(debate, speakers_dict):
    parts = combine_speakers(debate['parts'])

    candidates = set(debate['candidates'])
    other_speakers = set(debate['other_speakers'])
    for part in parts:
        for i, line in enumerate(part):
            # TODO: beef up
            line['question'] = line['speaker'] in other_speakers and '?' in line['text']

            if line['speaker'] in candidates and not line['question']:
                # find the last question asked
                # TODO: limit to last 15
                for x in range(i-1, -1, -1):
                    if part[x]['question']:
                        line['response'] = x
                        part[x]['response'].append(i)
                        break

                # TODO: if the previous wasnt a question, but was significant
                if 'response' not in line:
                    line['response'] = i - 1
                    part[i-1]['response'].append(i)
            else:
                line['response'] = []

    return parts


url = 'debates/december-democratic-debate-transcript-sixth-debate-from-los-angeles.txt'
with open(url) as f:
    debate = json.load(f)

# a dictionary mapping partial names to the full names
speakers_dict = generate_speakers_dict(debate)

parts = annotate_question_response(debate, speakers_dict)
for part in parts:
    for i, line in enumerate(part):
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
#     # correct all text speakers to match the candidates/ other_speakers fields
#     # fix_addressing(debate, speakers_dict)
#
#     with open(folder + file_name, 'w') as f:
#         f.write(json.dumps(debate, default=str))
