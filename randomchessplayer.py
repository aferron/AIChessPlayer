from aichessboard import AIChessBoard
from chess import Move
from chessplayer import ChessPlayer
import random
from typing import Any

class RandomChessPlayer(ChessPlayer):
    def __init__(self, time: Any) -> None:
        super().__init__(time)

    def _ChessPlayer__get_next_move(self, board: AIChessBoard) -> Move:
        legalmoves = list(board.legal_moves)
        if len(legalmoves) < 1:
            raise self.ChessPlayerException("No legal moves remain")
        return random.choice(legalmoves)
