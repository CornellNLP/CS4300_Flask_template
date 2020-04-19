import re
from collections import Counter
import csv

def load_word_weight(lexicon_file):
    ## Create a mapping from words to numbers
    word_weights = {}
    with open(lexicon_file) as lexicon_reader:
        for line in lexicon_reader:
            weight, word = line.rstrip().split(",") ## split on comma
            word_weights[word] = float(weight) ## convert string to number

    return word_weights

#load sentiment weights
word_weights = load_word_weight("data_code/syuzhet.csv")

## This function applies the word weights to a list of word counts
def score_counts(counter, word_weights):
    ## accumulate word weights in this variable
    score = 0

    ## count the words in the passage
    total_tokens = sum(counter.values())
    ## check for empty segments
    if total_tokens == 0:
        return 0

    ## for each word, look up its score
    for word in counter.keys():
        if word in word_weights:
            score += word_weights[word] * counter[word]
    return score/total_tokens #dividing by length of the doc, looking at short sentences instead of long paragraphs

#word pattern for tokenizing
word_pattern = re.compile("[\w\-]+") #re looking for 1+ letters or numbers, square brackets define a set of charaters

#make list of states
state_list = []
with open("data_code/governors_twitter_info.csv") as info:
    reader = csv.reader(info)
    next(reader)

    for line in reader:
        state_list.append(line[0])

#function to get tweet sentiment for every comment
def compile_comment_sent(state_list):
    all_states = {}
    for state in state_list:
        try:
            with open("data_code/comment_data/" + str(state) + ".csv") as state_file:
                reader = csv.reader(state_file)
                state_dict = {}
                next(reader)
                for tweet in reader:
                    date = tweet[3].replace("/", ".")
                    time = tweet[4].replace(":", ".")
                    all_time = date+ "." + time

                    link = tweet[19]

                    tokens = word_pattern.findall(tweet[10])
                    token_counts = Counter(tokens)

                    sentiment = score_counts(token_counts, word_weights)

                    state_dict[all_time] = (sentiment, link)
            all_states[state] = state_dict
        except FileNotFoundError:
            continue
    return all_states

#get dictionary of all comment sentiment data
comment_sentiment = compile_comment_sent(state_list)
