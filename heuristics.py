import chess
from chess import *
from enum import Enum

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



    def number_of_pieces_greater_than_opponent(self, board: List) -> int:
        # Takes the number of pawns and queens of the Player and subtracts the opponents pieces
        number_of_pawns: int = len(board.pieces(chess.PAWN, chess.WHITE)) * 1
        number_of_queens: int = len(board.pieces(chess.QUEEN, chess.WHITE)) * 100
        number_of_opponent_pawns: int = len(board.pieces(chess.PAWN, chess.BLACK)) * 1
        number_of_opponent_queens: int = len(board.pieces(chess.QUEEN, chess.BLACK)) * 100

        return ((number_of_pawns + number_of_queens) - (number_of_opponent_pawns + number_of_opponent_queens))


    def create_matrix_from_board(self, board: Board) -> int:
        epd: str = board.epd() 
        pieces = epd.split(" ", 1)[0] 
        rows = pieces.split("/")
        final_board = []
        for row in rows: 
            current_row = []
            for square in row:
                if square.isdigit(): 
                    for counter in range(0, int(square)):
                        current_row.append(".")
                else:
                    if(square == 'p'):
                        current_row.append(chess.BLACK)
                    else:
                        current_row.append(chess.WHITE)
            final_board.append(current_row)
        return final_board

    def pawn_chain_support(self, matrix_board: List) -> int: 
        heuristic_value = 0
        for counter, row in enumerate(matrix_board):
            if(counter == 0): 
                continue
            for element, square in enumerate(row):
                if(square == chess.WHITE):
                    if(element > 0 and (matrix_board[counter - 1][element - 1] == chess.WHITE)):
                        heuristic_value += 1
                    if(element < len(row) - 1 and (matrix_board[counter - 1][element + 1] == chess.WHITE)):
                        heuristic_value += 1
        return heuristic_value

    def pawn_side_by_side_support(self, matrix_board: List) -> int:
        heuristic_value = 0
        for counter, row in enumerate(matrix_board):
            for element, square in enumerate(row):
                if(square == chess.WHITE):
                    if(element > 0 and (matrix_board[counter][element - 1] == chess.WHITE)):
                        heuristic_value += 1
                    if(element < len(row) - 1 and (matrix_board[counter][element + 1] == chess.WHITE)):
                        heuristic_value += 1
        return heuristic_value

    def distance_from_opposite_side_of_board(self, matrix_board: List) -> int:
        heuristic_value = 0
        length_of_board = len(matrix_board)
        for counter, row in enumerate(matrix_board):
            if(counter > (length_of_board - 2)):
                continue
            for square in row:
                if(square == chess.WHITE):
                    heuristic_value += (length_of_board - counter - 2) 
        return heuristic_value * 5

    def number_of_stacked_pawns(self, matrix_board: List) -> int:
        heuristic_value = 0
        for counter, row in enumerate(matrix_board):
            if(counter == 0): # skip the back row since there will be no pawns behind them 
                continue
            for element, square in enumerate(row):
                if(square == chess.WHITE):
                    if(matrix_board[counter - 1][element] == chess.WHITE):
                        heuristic_value -= 1
        return heuristic_value

    def is_piece_at_risk(self, matrix_board: List) -> int:
        heuristic_value: int = 0
        for counter, row in enumerate(matrix_board):
            if(counter == 0): # skip the back row since there will be no pawns behind them 
                continue
            for element, square in enumerate(row):
                if(square == chess.WHITE):
                    if(element > 0):
                        if(matrix_board[counter - 1][element - 1] == chess.BLACK):
                            heuristic_value -= 20
                    if(element < len(row) - 1):
                        if(matrix_board[counter - 1][element + 1] == chess.BLACK):
                            heuristic_value -= 20
        return heuristic_value


