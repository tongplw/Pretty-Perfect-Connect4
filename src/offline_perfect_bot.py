import pandas as pd
import numpy as np

df = pd.read_csv('data/perfect_cache.csv')
d = df.set_index('k').to_dict()['v']

def get_perfect_move(game):
    board = game.board
    
    k = ''.join(map(str, board.ravel().tolist()))
    if k in d:
        return d[k]
    k2 = ''.join(map(str, board[:,::-1].ravel().tolist()))
    if k2 in d:
        return 6 - d[k2]
    print('miss')
    return np.random.choice(game.column_counts)