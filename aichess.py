import chess
from chess import Move

class CustomBoard(chess.Board):
    def outcome(self):
        black_pieces = self.occupied_co[chess.BLACK]
        white_pieces = self.occupied_co[chess.WHITE]
        black_wins = black_pieces & chess.BB_BACKRANKS != 0
        white_wins = white_pieces & chess.BB_BACKRANKS != 0
        
        if black_wins:
            return chess.Outcome(8, 0)
        elif white_wins:
            return chess.Outcome(8, 1)
        else:
            return None

    def print_binary_examples(self):
        print()
        print("white pieces: {0:b}".format(self.occupied_co[chess.WHITE]))
        print("black pieces: {0:b}".format(self.occupied_co[chess.BLACK]))
        print("backranks: {0:b}".format(chess.BB_BACKRANKS))
        print("pawns: {0:b}".format(self.pawns))
        print("pawns & backranks: {0:b}".format(self.pawns & chess.BB_BACKRANKS))


board = CustomBoard('8/pppppppp/8/8/8/8/PPPPPPPP/8')
print("start game\n", board, "\n")

def make_a_move(move_from: chess.Square, move_to: chess.Square):
    board.push(Move(move_from, move_to))
    print(board, "\n")
    outcome = board.outcome()
    if outcome != None:
        print("white" if outcome.winner else "black", " wins")

def run_example_game():
    make_a_move(chess.A2, chess.A4)
    make_a_move(chess.B7, chess.B5)
    make_a_move(chess.A4, chess.B5)
    make_a_move(chess.A7, chess.A5)
    make_a_move(chess.B5, chess.B6)
    make_a_move(chess.C7, chess.B6)
    make_a_move(chess.E2, chess.E4)
    make_a_move(chess.A5, chess.A4)
    make_a_move(chess.B2, chess.B4)
    make_a_move(chess.A4, chess.A3)
    make_a_move(chess.E4, chess.E5)
    make_a_move(chess.A3, chess.A2)
    make_a_move(chess.F2, chess.F4)
    make_a_move(chess.A2, chess.A1)

run_example_game()
board.print_binary_examples()