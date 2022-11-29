import chess
from chess import *
from enum import Enum
import numpy as np

# Using global variables to avoid chess library calls.
PLAYER_WHITE = chess.WHITE
PLAYER_BLACK = chess.BLACK
BOARD_SIZE = 64

class Heuristic(Enum):
    Maximize_Number_Of_Pieces = 0
    Keep_Pawns_Diagonally_Supported = 1
    Side_By_Side_Pawns = 2
    Distance_From_Starting_Location = 3
    Stacked_Pawns = 4
    Piece_Could_Be_Captured = 5

class Heuristics:
    def __init__(self, list_of_heuristics: list(Heuristic) ):
        self.List_of_Heuristics: list(Heuristic) = list_of_heuristics

    def return_heuristic_value(self, board: Board) -> int:
        matrix_board = self.create_matrix_from_board(board)
        heuristic_value: int = 0
        for heuristic in self.List_of_Heuristics:
                if heuristic == Heuristic.Maximize_Number_Of_Pieces:
                    heuristic_value += self.number_of_pieces_greater_than_opponent(board)
                elif heuristic == Heuristic.Keep_Pawns_Diagonally_Supported:
                    heuristic_value += self.pawn_chain_support(matrix_board)
                elif heuristic == Heuristic.Side_By_Side_Pawns:
                    heuristic_value += self.pawn_side_by_side_support(matrix_board)
                elif heuristic == Heuristic.Distance_From_Starting_Location:
                    heuristic_value += self.distance_from_opposite_side_of_board(matrix_board)
                elif heuristic == Heuristic.Stacked_Pawns:
                    heuristic_value += self.number_of_stacked_pawns(matrix_board)
                elif heuristic == Heuristic.Piece_Could_Be_Captured:
                    heuristic_value += self.is_piece_at_risk(matrix_board)
        return heuristic_value

    def number_of_pieces_greater_than_opponent(self, board: np.array) -> int:
        # Takes the number of pawns and queens of the Player and subtracts the opponents pieces
        number_of_pawns: int = len(board.pieces(chess.PAWN, PLAYER_WHITE)) * 1
        number_of_queens: int = len(board.pieces(chess.QUEEN, PLAYER_WHITE)) * 100
        number_of_opponent_pawns: int = len(board.pieces(chess.PAWN, PLAYER_BLACK)) * 1
        number_of_opponent_queens: int = len(board.pieces(chess.QUEEN, PLAYER_BLACK)) * 100
        return ((number_of_pawns + number_of_queens) - (number_of_opponent_pawns + number_of_opponent_queens))

    def create_matrix_from_board(self, board: Board) -> int:
        # Get black and white pieces.
        white = self.int_to_array(board.occupied_co[0], 'white')
        black = self.int_to_array(board.occupied_co[1], 'black')
        # Combine them with a mask.
        white[np.where(black is PLAYER_BLACK)] = PLAYER_BLACK
        mask = (white == ".")
        white[mask] = black[mask]
        return white

    def int_to_array(self, number, color):
        player = PLAYER_WHITE if color == 'white' else PLAYER_BLACK
        binary = ["." if int(x) == 0 else player for x in bin(number)[2:]]
        length = BOARD_SIZE - len(binary)
        padding = ["."] * length
        binary = (*padding, *binary) # appending this way requires python >= 3.5
        board_array = np.reshape(binary, (8,8))
        return np.flip(board_array, axis=0)


    def pawn_chain_support(self, matrix_board: np.array) -> int:
        heuristic_value = 0
        for counter, row in enumerate(matrix_board):
            if(counter == 0):
                continue
            for element, square in enumerate(row):
                if(square == PLAYER_WHITE):
                    if(element > 0 and (matrix_board[counter - 1][element - 1] == PLAYER_WHITE)):
                        heuristic_value += 1
                    if(element < len(row) - 1 and (matrix_board[counter - 1][element + 1] == PLAYER_WHITE)):
                        heuristic_value += 1
        return heuristic_value

    def pawn_side_by_side_support(self, matrix_board: np.array) -> int:
        heuristic_value = 0
        for counter, row in enumerate(matrix_board):
            for element, square in enumerate(row):
                if(square == PLAYER_WHITE):
                    if(element > 0 and (matrix_board[counter][element - 1] == PLAYER_WHITE)):
                        heuristic_value += 1
                    if(element < len(row) - 1 and (matrix_board[counter][element + 1] == PLAYER_WHITE)):
                        heuristic_value += 1
        return heuristic_value

    def distance_from_opposite_side_of_board(self, matrix_board: np.array) -> int:
        heuristic_value = 0
        length_of_board = len(matrix_board)
        for counter, row in enumerate(matrix_board):
            if(counter > (length_of_board - 2)):
                continue
            for square in row:
                if(square == PLAYER_WHITE):
                    heuristic_value += (length_of_board - counter - 2)
        return heuristic_value * 5

    def number_of_stacked_pawns(self, matrix_board: np.array) -> int:
        heuristic_value = 0
        for counter, row in enumerate(matrix_board):
            if(counter == 0): # skip the back row since there will be no pawns behind them
                continue
            for element, square in enumerate(row):
                if(square == PLAYER_WHITE):
                    if(matrix_board[counter - 1][element] == PLAYER_WHITE):
                        heuristic_value -= 1
        return heuristic_value

    def is_piece_at_risk(self, matrix_board: np.array) -> int:
        heuristic_value: int = 0
        for counter, row in enumerate(matrix_board):
            if(counter == 0): # skip the back row since there will be no pawns behind them
                continue
            for element, square in enumerate(row):
                if(square == PLAYER_WHITE):
                    if(element > 0):
                        if(matrix_board[counter - 1][element - 1] == PLAYER_BLACK):
                            heuristic_value -= 20
                    if(element < len(row) - 1):
                        if(matrix_board[counter - 1][element + 1] == PLAYER_BLACK):
                            heuristic_value -= 20
        return heuristic_value
