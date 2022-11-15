from aichessboard import AIChessBoard
from chess import Move
from chessplayer import ChessPlayer
import random

class RandomChessPlayer(ChessPlayer):
    def get_next_move(self, board: AIChessBoard) -> Move:
        legalmoves = list(board.legal_moves)
        if len(legalmoves) < 1:
            raise self.ChessPlayerException("No legal moves remain")
        return random.choice(legalmoves)
