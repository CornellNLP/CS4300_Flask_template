import json
import os

from app import debates_table


def insert_many(replace, folders=None):
    if replace:
        # delete everything in the database
        debates_table.delete_many({})

    if folders is None:
        folders = ['debates/', 'others/']
    # read all the json files in
    for folder in folders:
        for file_name in os.listdir(folder):
            with open(folder + file_name) as f:
                debate = json.load(f)

                # delete any debates with same url (redundant if replace)
                debates_table.delete_many({'url': debate['url']})
                # and insert them
                debates_table.insert_one(debate)


def insert_one(file_name):
    # read the debate in as a dictionary
    with open(file_name) as f:
        debate = json.load(f)

    # delete any debates with same url
    debates_table.delete_many({'url': debate['url']})
    # insert new one
    debates_table.insert_one(debate)


def delete_one(url):
    # delete any debates with same url
    debates_table.delete_many({'url': url})
