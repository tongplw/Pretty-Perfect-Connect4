import bot
import perfect_bot
import numpy as np
from scipy.signal import convolve2d


class Connect4:
    
    horizontal_kernel = np.array([[1, 1, 1, 1]])
    vertical_kernel = np.transpose(horizontal_kernel)
    diag1_kernel = np.eye(4, dtype=np.uint8)
    diag2_kernel = np.fliplr(diag1_kernel)
    kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]
    
    def __init__(self, game=None):
        self.height = 6
        self.width = 7
        self.game_over = False
        self.winner = 0
        
        # create a new board or use the old one
        if game is None:
            self.board = np.zeros((self.height, self.width), np.int8)
            self.turn = 1
        else:
            self.board = game.board.copy()
            self.turn = game.turn
        self.column_counts = np.count_nonzero(self.board, axis=0)
    
    def copy(self):
        return Connect4(self)
    
    def print_board(self):
        print(self.board)
    
    def play_turn(self, column, is_human=True):
        if column < 0 or column > self.width - 1:
            print(self.board, column)
            print('Invalid Column')
            return

        fill = self.column_counts[column]
        if fill > self.height - 1:
            print('Column is already filled')
            return

        self.board[self.height-1-fill][column] = self.turn
        self.column_counts[column] += 1
        self.check_win()
        self.turn = 3 - self.turn
    
    def check_win(self):
        for kernel in Connect4.kernels:
            if (convolve2d(self.board == self.turn, kernel, mode="valid") == 4).any():
                self.game_over = True
                self.winner = self.turn
                return

    # def play_with_bot(self):
    #     while not self.game_over:
    #         if self.turn == 1:
    #             column = int(input('Enter column to insert piece: '))
    #             self.play_turn(column)
    #             self.print_board()
    #         else:
    #             print('Bot Turn')
    #             best_move = bot.run(self)
    #             self.play_turn(best_move, is_human=False)
    #             self.print_board()
    #     print(f'Player {self.winner} Won!')
        
    # def play_with_friend(self):
    #     while not self.game_over:
    #         column = int(input('Enter column to insert piece: '))
    #         self.play_turn(column)
    #         self.print_board()
    #     print(f'Player {self.winner} Won!')
    
    def play_with_perfect_bot(self):
        while not self.game_over:
            if self.turn == 1:
                print('Player Turn')
                column = int(input('Enter column to insert piece: '))
                self.play_turn(column)
                self.print_board()
            else:
                print('Perfect Bot Turn')
                best_move = perfect_bot.get_perfect_move(self)
                self.play_turn(best_move, is_human=False)
                self.print_board()
        print(f'Player {self.winner} Won!')
        
    def test_bot(self):
        while not self.game_over:
            if self.turn == 1:
                print('Bot Turn')
                best_move = bot.run(self)
                self.play_turn(best_move, is_human=False)
                self.print_board()
            else:
                print('Perfect Bot Turn')
                best_move = perfect_bot.get_perfect_move(self)
                self.play_turn(best_move, is_human=False)
                self.print_board()
        print(f'Player {self.winner} Won!')
    
    def perfect_bot_with_perfect_bot(self):
        while not self.game_over:
            if self.turn == 1:
                print('Perfect Bot 1 Turn')
                best_move = perfect_bot.get_perfect_move(self, cache=True)
                self.play_turn(best_move, is_human=False)
                self.print_board()
            else:
                print('Perfect Bot 2 Turn')
                best_move = perfect_bot.get_perfect_move(self, cache=False)
                self.play_turn(best_move, is_human=False)
                self.print_board()
        print(f'Player {self.winner} Won!')

if __name__ == '__main__':
    for i in range(10):
        game = Connect4()
        # game.play_with_perfect_bot()
        # game.test_bot()
        game.perfect_bot_with_perfect_bot()