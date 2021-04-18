import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def boardgame_jaccard(game_title, boardgame_data):
    boardgames_df = pd.read_csv(boardgame_data)
    
    shape = boardgames_df.shape
    num_boardgames = shape[0]
    sims_jac = []
    
    try:
        index = boardgames_df.index
        game_index = index[boardgames_df['primary'] == game_title]
        game_genres = boardgames_df.at[game_index[0], 'boardgamecategory'][1:-1].replace("'", "")
        game_genres = set(game_genres.split(','))
    except TypeError:
        game_genres = []
    
    for i in range(num_boardgames):
        try:
            cat_i = boardgames_df.at[i,'boardgamecategory'][1:-1].replace("'", "")
            cat_i = set(cat_i.split(','))
        except TypeError:
            cat_i = []
        if boardgames_df.at[i,'primary'] != game_title:
            if len(cat_i) == 0 or len(game_genres) == 0:
                sims_jac.append((boardgames_df.at[i,'primary'],0))
            else:
                sims_jac.append((boardgames_df.at[i,'primary'],(len(cat_i & game_genres) / len(cat_i | game_genres))))
        
    return sorted(sims_jac, key=lambda x: -x[1])

def boardgame_cosine_sim(game_title, boardgame_data):
    boardgames_df = pd.read_csv(boardgame_data)
    shape = boardgames_df.shape
    num_boardgames = shape[0]
    cosine_sims = []
    
    index = boardgames_df.index
    game_index = index[boardgames_df['primary'] == game_title]
    game_desc = boardgames_df.at[game_index[0], 'description']
    
    tfidf_vec = TfidfVectorizer(stop_words="english")
    descriptions = []
    for i in range(num_boardgames):
        script_i = boardgames_df.at[i, 'description']
        if pd.isnull(script_i):
            descriptions.append('')
        else:
            descriptions.append(script_i)
        
    tfidf_mat = tfidf_vec.fit_transform(descriptions).toarray()
    
    for i in range(num_boardgames):
        q = tfidf_mat[i]
        d = tfidf_mat[game_index[0]]
        if boardgames_df.at[i,'primary'] != game_title:
            if np.linalg.norm(q) * np.linalg.norm(d) == 0:
                cosine_sims.append((boardgames_df.at[i,'primary'], 0))
            else:
                cosine_sims.append((boardgames_df.at[i,'primary'], (np.dot(q, d)) / (np.linalg.norm(q) * np.linalg.norm(d))))
    
    return sorted(cosine_sims, key=lambda x: -x[1])
        
        
def boardgames_boolean(similar_games, disliked_games, filter_genres, boardgame_data):
    boardgames_df = pd.read_csv(boardgame_data)
    filtered_games = []
    index = boardgames_df.index
    for game in similar_games:
        if game[0] not in disliked_games:
            game_index = index[boardgames_df['primary'] == game[0]]
            for genre in filter_genres:
                try:
                    if genre not in boardgames_df.at[game_index[0], 'boardgamecategory']:
                        filtered_games.append(game)
                except TypeError:
                    pass
                    
    return filtered_games
        
# print(boardgame_jaccard('XCOM: The Board Game', 'games_detailed_info.csv'))
# print(boardgame_cosine_sim('XCOM: The Board Game', 'games_detailed_info.csv'))
# game_list = boardgame_cosine_sim('XCOM: The Board Game', 'games_detailed_info.csv')
# print(boardgames_boolean(game_list, ['Metro 2033: Breakthrough'], ['Trivia'], 'games_detailed_info.csv'))