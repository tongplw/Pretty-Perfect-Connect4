import numpy as np
import pandas as pd

df = pd.read_csv('cache.csv')
d = df.set_index('k').to_dict()['v']

def run(game):
    return minimax(game, 6, -float('inf'), float('inf'), True)[1]

def minimax(game, depth, alpha, beta, player):
    game.check_win()
    if game.game_over:
        return terminal_state(game)
    if depth == 0:
        return get_score(game), None
    if player:
        return max_player(game, depth, alpha, beta, player)
    else:
        return min_player(game, depth, alpha, beta, player)

def terminal_state(game):
    if game.winner == 1:
        return -1e15, None
    if game.winner == 2:
        return 1e15, None
    return 0, None

def get_score(game):
    k = ''.join(map(str, game.board.ravel().tolist()))
    if k in d:
        return d[k]
    score = 0
    gcc = game.column_counts
    # horizontal
    for r in range(game.height):
        for c in range(game.width-3):
            values = game.board[r, c:c+4]
            x = np.minimum(gcc[c:c+4], [r]*4)
            space = r*4 - np.sum(x)
            score += evaluate_score(values, space)
    # vertical
    for r in range(game.height-3):
        for c in range(game.width):
            values = game.board[r:r+4, c]
            space = 1
            score += evaluate_score(values, space)
    # diagonal
    for r in range(game.height-3):
        for c in range(game.width-3):
            values = [game.board[r][c], game.board[r+1][c+1], game.board[r+2][c+2], game.board[r+3][c+3]]
            x = np.minimum(gcc[c:c+4], [r+i for i in range(4)])
            space = (4*r+6) - np.sum(x)
            score += evaluate_score(values, space)
    # diagonal2
    for r in range(3, game.height):
        for c in range(game.width-3):
            values = [game.board[r][c], game.board[r-1][c+1], game.board[r-2][c+2], game.board[r-3][c+3]]
            x = np.minimum(gcc[c:c+4], [r-i for i in range(4)])
            space = (4*r-6) - np.sum(x)
            score += evaluate_score(values, space)
    d[k] = score
    pd.DataFrame([[k, score]]).to_csv('cache.csv', mode='a', header=False)
    return score

def evaluate_score(array, space=0):
    bot = 0
    opp = 0
    for e in array:
        if e == 1:
            bot += 1
        elif e == 2:
            opp += 1
    if opp == 0:
        return 2 ** (2 ** bot) - space#* (100 + spaces)/100
    if bot == 0:
        return -(2 ** (2 ** opp) - space) #* (100 + spaces)/100)
    return 0

def viable_permutation(game):
    columns = np.flatnonzero(game.column_counts < game.height)
    np.random.shuffle(columns)
    return columns

def max_player(game, depth, alpha, beta, player):
    column = 0
    best_score = -float('inf')
    options = viable_permutation(game)
    for option in options:
        game_copy = game.copy()
        game_copy.play_turn(option, False)
        score = minimax(game_copy, depth-1, alpha, beta, False)[0]
        if score > best_score:
            best_score = score
            column = option
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    return best_score, column

def min_player(game, depth, alpha, beta, player):
    column = 0
    best_score = float('inf')
    options = viable_permutation(game)
    for option in options:
        game_copy = game.copy()
        game_copy.play_turn(option, False)
        score = minimax(game_copy, depth-1, alpha, beta, True)[0]
        if score < best_score:
            best_score = score
            column = option
        beta = min(beta, score)
        if alpha >= beta:
            break
    return best_score, column