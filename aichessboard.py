import chess

class AIChessBoard(chess.Board):
    def outcome(self) -> None:
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

    def print_binary_examples(self) -> None:
        print()
        print("white pieces: {0:b}".format(self.occupied_co[chess.WHITE]))
        print("black pieces: {0:b}".format(self.occupied_co[chess.BLACK]))
        print("backranks: {0:b}".format(chess.BB_BACKRANKS))
        print("pawns: {0:b}".format(self.pawns))
        print("pawns & backranks: {0:b}".format(self.pawns & chess.BB_BACKRANKS))

# simple_board_fen = '8/1p6/8/8/8/8/1p6/8'
# board = AIChessBoard(simple_board_fen)
# print(board)
# print()
# print(AIChessBoard())
# print(AIChessBoard().turn)
# print(AIChessBoard().legal_moves)