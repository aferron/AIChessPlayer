from  abc import ABC, abstractmethod
from aichessboard import AIChessBoard
from chess import Move

class ChessPlayer(ABC):

    @abstractmethod
    def get_next_move(self, board: AIChessBoard) -> Move:
        pass

    class ChessPlayerException(Exception):
        def __init__(self, message=''):
            self.message = 'Error in the ChessPlayer:' + message