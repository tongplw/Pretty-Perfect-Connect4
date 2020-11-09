from src.connect4 import Connect4

if __name__ == '__main__':
    while True:
        try:
            game = Connect4()
            # game.play_with_perfect_bot()
            # game.test_bot()
            game.perfect_bot_with_perfect_bot()
            # game.demo()
        except:
            pass