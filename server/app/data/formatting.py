import json
import os


IRRELEVANT_TEXT_BLOCK = 50
IMPORTANT_TEXT_BLOCK = 150


# dictionaries mapping partial names to the full names and reverse
def generate_speakers_dict(debate):
    speakers = set(debate['candidates'] + debate['other_speakers'])
    parts_to_name = dict()
    name_to_parts = dict()
    for name in speakers:
        # get all parts of the name
        name_to_parts[name] = set(name.lower().split(' '))
        # create a reverse dictionary: part of the name to full name
        for name_part in name_to_parts[name]:
            if name_part in parts_to_name:
                parts_to_name[name_part] = None
            else:
                parts_to_name[name_part] = name

    # remove names that can point to multiple people
    parts_to_name = {k: v for k, v in parts_to_name.items() if v is not None}
    return parts_to_name, name_to_parts


# correct all text speakers to match the candidates/ other_speakers fields
def fix_addressing(debate, parts_to_name):
    speakers = set(debate['candidates'] + debate['other_speakers'])
    for part in debate['parts']:
        for line in part['text']:
            # if name not already exactly matched
            if line['speaker'] not in speakers:
                name = None
                for name_part in line['speaker'].lower().split(' '):
                    if name_part in parts_to_name:
                        line['speaker'] = parts_to_name[name_part]
                        break
                # if name can't be matched, must be done manually
                if line['speaker'] is None:
                    raise Exception('Debate ' + debate['url'] + '\nName ' + line['speaker'] + ' cannot be matched')
    return parts_to_name, debate


# add whether they are questions
def annotate_questions(debate):
    other_speakers = set(debate['other_speakers'])
    for part in debate['parts']:
        for i, line in enumerate(part['text']):
            # if not a candidate and has question mark or is long
            line['question'] = line['speaker'] in other_speakers and ('?' in line['text'] or len(line['text']) > IMPORTANT_TEXT_BLOCK)


# combining same speaker blocks together
def combine_speakers(debate):
    for i, part in enumerate(debate['parts']):
        # checks previous speaker, so initialize the list with fake one
        new_transcript = [{'speaker': None}]
        for line in part['text']:
            # if matches previous quote, combine
            if line['speaker'] == new_transcript[-1]['speaker']:
                new_transcript[-1]['text'] += ' ' + line['text']
            else:
                new_transcript.append(line)
        debate['parts'][i]['text'] = new_transcript[1:]


# combine candidates' responses when they are cutoff but keep talking
def combine_speakers_interrupting(debate):
    candidates = set(debate['candidates'])
    for i, part in enumerate(debate['parts']):
        # checks previous two speakers, so initialize the list with fake ones
        new_transcript = [{'speaker': None}, {'speaker': None}]
        for line in part['text']:
            prev_quote = new_transcript[-1]
            prev_prev_quote = new_transcript[-2]

            # candidate continuing to speak
            a = line['speaker'] == prev_prev_quote['speaker'] and line['speaker'] in candidates and len(prev_prev_quote['text']) > IMPORTANT_TEXT_BLOCK
            # wouldn't delete anything important
            b = a and not prev_quote['question'] and len(prev_quote['text']) < IRRELEVANT_TEXT_BLOCK
            if b:
                # delete previous speaker
                new_transcript.pop()
                # combine with 2 speakers back
                prev_prev_quote['text'] += ' ' + line['text']
                prev_prev_quote['question'] = prev_prev_quote['question'] or line['question']
            else:
                new_transcript.append(line)
        debate['parts'][i]['text'] = new_transcript[2:]


# link questions and responses together
def annotate_responses(debate):
    candidates = set(debate['candidates'])
    other_speakers = set(debate['other_speakers'])
    for part in debate['parts']:
        for i, line in enumerate(part['text']):
            if i == 0 and line['speaker'] in candidates and not line['question']:
                raise Exception('Debate ' + debate['url'] + '\nText has no response: ' + line['text'])
            else:
                prev_quote = part['text'][i-1]
                # if candidate, need to find what quote responding to
                if line['speaker'] in candidates and not line['question']:
                    # if responding to another candidate
                    if prev_quote['speaker'] in candidates and len(prev_quote['text']) > IRRELEVANT_TEXT_BLOCK:
                        line['response'] = i-1
                    # TODO: more advanced response to another candidate
                    # elif part['text'][i-2]['speaker'] in candidates and [x for x in name_to_parts[line['speaker']] if x in part['text'][i-2]['text'].lower()]:
                    else:
                        # otherwise find the last question asked
                        for x in range(i-1, -1, -1):
                            if part['text'][x]['question']:
                                line['response'] = x
                                part['text'][x]['response'].append(i)
                                break

                    # if couldn't identify response, find the last other speaker
                    if 'response' not in line:
                        for x in range(i-1, -1, -1):
                            if part['text'][x]['speaker'] in other_speakers:
                                line['response'] = x
                                part['text'][x]['response'].append(i)
                                break

                    # if really can't match
                    if 'response' not in line:
                        raise Exception('Debate ' + debate['url'] + '\nText has no response: ' + line['text'])
                else:
                    # initialize list of responses to be filled in
                    line['response'] = []


def format_and_annotate(debate):
    dict_parts_to_name, dict_name_to_parts = generate_speakers_dict(debate)
    fix_addressing(debate, dict_parts_to_name)
    combine_speakers(debate)
    annotate_questions(debate)  # needs length of response
    combine_speakers_interrupting(debate)  # needs whether it's a question
    annotate_responses(debate)


folders = ['debates/', 'others/']
for folder in folders:
    for file_name in os.listdir(folder):
        with open(folder + file_name) as f:
            debate_dictionary = json.load(f)

        format_and_annotate(debate_dictionary)

        with open(folder + file_name, 'w', encoding='utf8') as f:
            json.dump(debate_dictionary, f, default=str, ensure_ascii=False)


# # Testing Code
# # load the files
# with open('debates/december-democratic-debate-transcript-sixth-debate-from-los-angeles.json') as f:
#     debate_dictionary = json.load(f)
# with open('coded.json') as f:
#     correct = json.load(f)
#
# # do all formatting
# format_and_annotate(debate_dictionary)
#
# # TODO: remove name? from being a question,
# #  fine tune the length of a question
# # TODO: responding
# #  if say name (with titles) and then respond two ago -> response
#
# # how many were coded correctly
# total = 0
# wrong = 0
# candidates = set(debate_dictionary['candidates'])
# for x, part in enumerate(debate_dictionary['parts']):
#     for y, line in enumerate(part['text']):
#         # only check relevant quotes
#         if correct['parts'][x]['text'][y]['speaker'] in candidates or correct['parts'][x]['text'][y]['response'] or line['response']:
#             # total += len(line['text'])
#             total += 1
#             if line['question'] != correct['parts'][x]['text'][y]['question']:
#             # if line != correct['parts'][x]['text'][y]:
#             #     wrong += len(line['text'])
#                 wrong += 1
#
# print(wrong / total)
