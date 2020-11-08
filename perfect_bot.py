import time
import random
import requests
import numpy as np
import pandas as pd

URL = 'http://connect4.ist.tugraz.at:8080/moveinfo'

df = pd.read_csv('perfect_cache.csv')
d = df.set_index('k').to_dict()['v']

def get_perfect_move(game, cache=False):
    board = game.board
    
    if cache:
        k = ''.join(map(str, board.ravel().tolist()))
        if k in d:
            return d[k]
        k2 = ''.join(map(str, board[:,::-1].ravel().tolist()))
        if k2 in d:
            return 6 - d[k2]

    board = np.array(board[::-1], dtype=object)
    board[board == 0] = "e"
    board[board == 1] = "a"
    board[board == 2] = "b"
    board = str(board.tolist()).replace("'", '"')
    
    data = {
        'board': board,
        'player': 'a' if game.turn == 1 else 'b',
        'timestamp': int(time.time() * 1000),
        'uuid': '40c9b1c5-29db-2e35-5b68-053b6e468d7f'
    }

    r = requests.post(URL, data=data)
    move_info = r.json()['moveInfos']
    
    best_val = 999
    best_col = -1
    
    # check for best winning move (lower score)
    for index, value in enumerate(move_info):
        if value != 0 and value != 200 and (value % 2 == 0 or value < 0):
            if (value < best_val):
                best_val = value
                best_col = index
            
    # check for draw move, if no winning move was found
    if best_col == -1:
        best_val = -999
        for index, value in enumerate(move_info):
            if value == 200:
                best_val = value
                best_col = index
    
    # check for best losing move, if no col has been selected yet
    if best_col == -1:
        best_val = -999
        for index, value in enumerate(move_info):
            if value != 0 and value > best_val:
                best_val = value
                best_col = index
    
    res_cols = []
    for index, value in enumerate(move_info):
        if value == best_val:
            res_cols += [index]
    
    # Choose a random best column
    if len(res_cols) > 0:
        best_col = random.choice(res_cols)

    if cache:
        d[k] = best_col
        pd.DataFrame([[k, best_col]]).to_csv('perfect_cache.csv', mode='a', header=False, index=False)
    
    return best_col