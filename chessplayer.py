from  abc import ABC, abstractmethod
from aichessboard import AIChessBoard
from chess import Move

class ChessPlayer(ABC):

    def __init__(self) -> None:
        self.__name = self.__class__.__name__

    def get_name(self) -> str:
        return self.__name

    @abstractmethod
    def get_next_move(self, board: AIChessBoard) -> Move:
        pass

    class ChessPlayerException(Exception):
        def __init__(self, message=''):
            self.message = 'Error in the ChessPlayer:' + message