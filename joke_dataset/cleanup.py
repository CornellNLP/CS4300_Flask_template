# Run file to remove "edit:" from reddit json files
import json
import re

# I change this depending on what kind of 'edit' styles are still left
edit_regex = re.compile('\\n(.*?)edit') # change regex based on what 'edits' are still in the file

def cleanup():
    data = None # holds the current version
    with open('./json/data_nopreprocess/reddit_jokes.json') as f:
        data = json.load(f)
    for obj in range(len(data)):
        joke = data[obj]['joke']
        edit = edit_regex.search(joke) #substring captured by regex
        if edit != None:
            edit = edit.group(0)
            idx = joke.find(edit)
            if idx != -1:
                # replaces joke with the same joke removing everything after the matching regex
                data[obj]['joke'] = joke[:idx]
                print(joke[:idx])

    # re-write the folder to continue edit
    with open('./json/data_nopreprocess/reddit_jokes_noedits.json', 'w') as f:
        json.dump(data, f, indent=4)

cleanup()
