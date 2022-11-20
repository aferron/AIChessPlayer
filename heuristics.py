import chess
from chess import *

class Heurstics: 

    def number_of_pieces_greater_than_opponent(self, board: Board, player_color: chess.Color):
        # Takes the number of pawns and queens of the Player and subtracts the opponents pieces
        number_of_pawns: int = len(board.pieces(chess.PAWN, player_color)) * 1
        number_of_queens: int = len(board.pieces(chess.QUEEN, player_color)) * 10
        number_of_opponent_pawns: int = len(board.pieces(chess.PAWN, (chess.WHITE if player_color == chess.BLACK else chess.BLACK))) * 1
        number_of_opponent_queens: int = len(board.pieces(chess.QUEEN, (chess.WHITE if player_color == chess.BLACK else chess.BLACK))) * 10

        return (number_of_pawns + number_of_queens) - (number_of_opponent_pawns + number_of_opponent_queens)


    def create_matrix_from_board(self, board: Board):
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
        print(final_board)
        return final_board

    def pawn_chain_support(self, board: Board, player_color: chess.Color): 
        matrix_board = self.create_matrix_from_board(board)
        heuristic_value = 0
        for counter, row in enumerate(matrix_board):
            if(counter == 0 or len(matrix_board) - 1): # skip the back rows 
                continue
            for element, square in enumerate(row):
                if(square == player_color):
                    if(element > 0 and (matrix_board[counter - 1][element - 1] == player_color)):
                        heuristic_value += 2
                    if(element < len(row) - 1 and (matrix_board[counter - 1][element + 1] == player_color)):
                        heuristic_value += 2
        return heuristic_value

    def pawn_side_by_side_support(self, board: Board, player_color: chess.Color):
        matrix_board = self.create_matrix_from_board(board)
        heuristic_value = 0
        for counter, row in enumerate(matrix_board):
            for element, square in enumerate(row):
                if(square == player_color):
                    if(element > 0 and (matrix_board[counter][element - 1] == player_color)):
                        heuristic_value += 1
                    if(element < len(row) - 1 and (matrix_board[counter][element + 1] == player_color)):
                        heuristic_value += 1
        return heuristic_value
