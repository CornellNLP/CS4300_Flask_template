# This script was used once to produce winemag_data_withtoks. This script
# creates a toks filed that is the tokenized description. Additionally, it
# deletes the taster_name and taster_twitter_handle columns to save memory. It
# takes about 30-60 seconds to run.

import json
from nltk.tokenize import TreebankWordTokenizer
import pandas as pd


def tokenizer(query):
    """
    Returns list of tokens from query.
    """
    if query is None:
        query = ""
    return TreebankWordTokenizer().tokenize(query)


# Open json file
with open("winemag_data.json") as f:
    data = json.load(f)

# Convert to df and delete duplicate rows
df = pd.DataFrame(data)
df.drop_duplicates()

varieties = [
    'Mourvedre', 'Gamay', 'Cabernet Franc', 'Syrah', 'Petit Verdot', 'Barbera',
    'Nebbiolo', 'Grenache', 'Tempranillo', 'Sangiovese', 'Carmenere',
    'Moscato', 'Champagne', 'Pinot Noir', 'Pinot Grigio', 'Cabernet Sauvignon',
    'Chardonnary', 'Riesling', 'Ros\u00e9', 'Malbec', 'White Zinfandel',
    'Sauvignon Blanc', 'Merlot'
]
df = df[df['variety'].isin(varieties)]
df = df.sample(n=10000)
# Tokenize description and add to df as "toks"
toks = []
for i in df["description"]:
    toks.append(tokenizer(i))
df["toks"] = toks

# Delete useless columns
del df["taster_name"]
del df["taster_twitter_handle"]

print(df[:5])

# Write to file
df.to_json("winemag_data_withtoks.json")
