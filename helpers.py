
import chess
from chess import Move
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