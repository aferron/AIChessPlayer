
# Testing
game = Game()
minimax = False
for x in range(50):
    if x % 2 == 0:
        game.board.turn = chess.WHITE
    else:
        game.board.turn = chess.BLACK
    move = min_max(game, 4)
    if move == None:
        break
    game.board.push(move)
    print(move)
    print(game.board)