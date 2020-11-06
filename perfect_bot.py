import time
import random
import requests
import numpy as np

URL = 'http://connect4.ist.tugraz.at:8080/moveinfo'

def get_perfect_move(game):
    board = game.board
    board = np.array(board[::-1], dtype=object)
    board[board == 0] = "e"
    board[board == 1] = "a"
    board[board == 2] = "b"
    board = str(board.tolist()).replace("'", '"')
    
    data = {
        'board': board,
        'player': 'a' if game.turn == 1 else 'b',
        'timestamp': int(time.time() * 1000),
        'uuid': 'ccaf01f4-be3f-ccac-a99c-fefbf46e7fff'
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

    return best_col