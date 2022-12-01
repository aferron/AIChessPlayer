from  abc import ABC, abstractmethod
from aichessboard import AIChessBoard
from chess import Move
import time

class ChessPlayer(ABC):

    def __init__(self, time: time) -> None:
        self.__time = time
        self.__name = self.__class__.__name__
        self.total_moves = 0
        self.average_time_to_get_move = 0

    def get_name(self) -> str:
        return self.__name

    def get_next_move(self, board: AIChessBoard) -> Move:
        self.total_moves += 1
        start = self.__time.process_time()
        print(start)
        next_move = self.__get_next_move(board)
        end = self.__time.process_time()
        print(end)
        process_time = end - start
        print(process_time)
        self.average_time_to_get_move += (process_time - self.average_time_to_get_move) / self.total_moves
        print(self.average_time_to_get_move)
        return next_move

    @abstractmethod
    def __get_next_move(self, board: AIChessBoard) -> Move:
        pass

    class ChessPlayerException(Exception):
        def __init__(self, message=''):
            self.message = 'Error in the ChessPlayer:' + message