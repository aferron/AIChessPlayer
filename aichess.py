from aichessboard import AIChessBoard
import chess
from chess import Move
from heuristics import * 

class Game:
    def __init__(self) -> None:
        self.board = AIChessBoard('8/pppppppp/8/8/8/8/PPPPPPPP/8')
        self.heuristic = Heurstics()

    def __make_a_move(self, move_from: chess.Square, move_to: chess.Square) -> None:
        self.board.push(Move(move_from, move_to))
        print(self.board, "\n")
        outcome = self.board.outcome()
        if outcome != None:
            print("white" if outcome.winner else "black", " wins")

    def run_example_game(self) -> None:
        print("start game\n", self.board, "\n")
        self.__make_a_move(chess.A2, chess.A4)
        self.__make_a_move(chess.B7, chess.B5)
        self.__make_a_move(chess.A4, chess.B5)
        self.__make_a_move(chess.A7, chess.A5)
        self.__make_a_move(chess.B5, chess.B6)
        self.__make_a_move(chess.C7, chess.B6)
        self.__make_a_move(chess.E2, chess.E4)
        self.__make_a_move(chess.A5, chess.A4)
        self.__make_a_move(chess.B2, chess.B4)
        self.__make_a_move(chess.A4, chess.A3)
        self.__make_a_move(chess.E4, chess.E5)
        self.__make_a_move(chess.A3, chess.A2)
        self.__make_a_move(chess.F2, chess.F4)
        self.__make_a_move(chess.A2, chess.A1)

game = Game()
game.run_example_game()
game.board.print_binary_examples()