from aichessboard import AIChessBoard
import chess
from chess import Move
from chessplayer import ChessPlayer


class Game:
    def __init__(self, white: ChessPlayer, black: ChessPlayer, visual: bool, verbose: bool) -> None:
        self.player_white = white
        self.player_black = black
        self.__visual = visual
        self.__verbose = verbose
        self.board = AIChessBoard('8/pppppppp/8/8/8/8/PPPPPPPP/8')
        self.terminated = False
        self.winner: bool = None

    def __make_a_move(self, move: Move) -> None:
        if move != None:
            self.board.push(move)
        if self.__visual:
            print(self.board, "\n")
        outcome = self.board.outcome()
        if outcome != None:
            self.terminated = True
            self.winner = outcome.winner
            if self.__verbose:
                print("white" if outcome.winner else "black", " wins")

    def run(self) -> ChessPlayer:
        while self.terminated is False:
            player = self.player_white if self.board.turn is True else self.player_black
            try:
                start_player_move_time = 0
                player_move = player.get_next_move(self.board)
                end_player_move_time = 1
                if player_move == None:
                    self.terminated = True
                    return None
                self.__make_a_move(player_move)
            except ChessPlayer.ChessPlayerException as e:
                self.terminated = True
                return None
        return self.winner

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
