import json
import re

edit_regex = re.compile('\\n(.*?)edit')

def cleanup():
    data = None
    with open('./json/reddit_jokes_noedits.json') as f:
        data = json.load(f)
    for obj in range(len(data)):
        joke = data[obj]['joke']
        edit = edit_regex.search(joke)
        if edit != None:
            edit = edit.group(0)
            idx = joke.find(edit)
            if idx != -1:
                data[obj]['joke'] = joke[:idx]
                print(joke[:idx])

    with open('./json/reddit_jokes_noedits.json', 'w') as f:
        json.dump(data, f, indent=4)

cleanup()
