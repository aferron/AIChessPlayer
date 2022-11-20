import chess
import numpy as np
from gmpy2 import popcount # arithmetic library



def board_to_array(board, desired_dims):
    """
    Return the configuration of pawns on the board as an array of 1s and 0s.
    Input: chess board, dimensional output desired (1 or 2)
    Output: An array of ints with selected dimensions and a count of pawns.
    """
    # One liner to count the number of 1s in a binary.
    count_ones = popcount(board.pawns) #imported from gmpy2
    binary = [int(x) for x in bin(board.pawns)[2:]]
    board_array = np.pad(binary, (64-(len(binary)),0),'constant')
    if desired_dims == 2:
        board_array = np.reshape(board_array, (8,8))
        return np.flip(board_array, axis=1), count_ones
    return board_array, count_ones



# Use this to recover the current binary map from a variable.
def int_to_array(number, desired_dims):
    """
    Return the configuration of pieces on the board as an array of 1s and 0s.
    Input: integer, dimensional output desired (1 or 2)
    Output: An array of ints with selected dimensions and a count of pieces.
    """
    # One liner to count the number of 1s in a binary.
    count_ones = popcount(number) #imported from gmpy2
    binary = [int(x) for x in bin(number)[2:]]
    board_array = np.pad(binary, (64-(len(binary)),0),'constant')
    if desired_dims == 2:
        board_array = np.reshape(board_array, (8,8))
        return np.flip(board_array, axis=1), count_ones
    return board_array, count_ones



def pawn_board_to_int(board_config):
        """
        Input: Any valid board configuration:
        Example: '8/pppppppp/8/8/8/8/PPPPPPPP/8'
        Output: A 64 bit integer encoded with board positions in binary.
        Use: doing a bitwise & with any board and the output will return
        0 if there is no overlap. Membership in a square can be checked.
        """
        return chess.Board(board_config).pawns