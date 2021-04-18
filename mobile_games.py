import pandas as pd
import re

mgs = pd.read_csv('googleplaystore.csv')


app_categories = mgs[‘category’]
booleans = []
for cat in app_categories:
    if not re.search('GAME', cat):
        booleans.append(False)
    else:
        booleans.append(True)

Filtered = pd.Series(booleans)
game_apps = mgs[Filtered]

mgs_sets = dict()
for i in range(len(game_apps['App'])):
    key = game_apps['App'][i]
    app_type = game_apps['Type'][i]
    content = game_apps['Content Rating'][i]
    genres = game_apps['Genres'][i].split(';')
    mgs_sets[key] = set(app_type) | set(content) | set(genres)


def mgs_jaccard(app1, app2):
    AintB = mgs_sets[app1].intersection(mgs_sets[app2])
    AuniB = mgs_sets[app1].union(mgs_sets[app2])
    return len(AintB) / len(AuniB)


def mgs_jaccard_list(app):
    score_list = []
    for k in game_apps['App']:
        if k != app:
            score_list.append((x, mgs_jaccard(app, k)))
    return score_list


def mgs_get_rankings(score_list):
    return sorted(score_list, key=lambda x: x[1], reverse=True)
