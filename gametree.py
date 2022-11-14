import numpy as np
from collections import deque
from dataclasses import dataclass, field
from typing import Any
from aichessboard import AIChessBoard
import chess
from chess import Move
from aichess import Game

"""
The purpose of this class is to serve as data storage for
State exploration. Comparison operators can be used to determine
reward. The dataclass feature requires python 3.7+.
"""

@dataclass(order=True)
class Node:
    reward:         int
    board:          Any=field(compare=False)
    move:           Any=field(compare=False)
    win_status:     Any=field(compare=False)

    def __init__(self, reward, board, move, win_status):
        self.reward = reward
        self.board = board
        self.move = move
        self.win_status = win_status
    def copy(self):
        return Node(self.reward, self.board, self.move, self.win_status)



def min_max(game):
    board = game.board
    minimax = False
    root = Node(0, board, None, None)
    solution_node = pre_order(game,root, minimax)
    return solution_node.move

# preorder DFS of binary tree. Minimax is a toggle switch, it's input must be False.
def pre_order(game, root, minimax):
    minimax = (minimax == False) # this will switch max and min on each call
    black_pieces = root.board.occupied_co[chess.BLACK]
    white_pieces = root.board.occupied_co[chess.WHITE]
    black_wins = 255  & black_pieces != 0
    white_wins = 18374686479671623680 & white_pieces != 0
    root_copy = root.copy()

    if  black_wins:
        return Node(1,root_copy.board,root_copy.move,-1)
    if white_wins:
        return Node(1,root_copy.board,root_copy.move,1)
    # if minimax == False:
    #     root_copy.board.turn = chess.WHITE
    # else:
    #     root_copy.board.turn = chess.BLACK

    children = unpack(root_copy, minimax) # we have the child nodes including rewards
    tree = list()

    if not children:
        return root_copy

    for child in children:
        # Recursive call to get next states
        child_node = pre_order(game, child, minimax)
        if child_node != None:
            # alpha beta pruning would go here
            tree.append(child_node)
            if child_node.win_status == 1:
                if root.board == game.board: #checking if this is the original root
                    return child_node
                else:
                    temp = Node(1,root_copy.board,root_copy.move,1)
                    return temp


    # There are no viable moves down this path.
    if not tree:
        return root_copy

    # It's maxes turn.
    if minimax == True:
        max_node = max(tree)
        max_node_t = Node(max_node.reward, root.board, root.move, max_node.win_status)
        return max_node_t
    # It's mins turn
    else:
        min_node = min(tree)
        min_node_t = Node(min_node.reward, root.board, root.move, min_node.win_status)
        return min_node_t


# use the minimax variable to switch players
def unpack(root, minimax):
    base_board = root.board
    legalmoves = list(root.board.legal_moves)
    nodes = []
    for move in legalmoves:
        board = base_board.copy()
        board.push(move)
        reward = calc_reward(board)
        win_status = 0 # This case is taken care of by recursive call
        nodes.append(Node(reward, board, move, win_status))
    if not nodes:
        return None
    return nodes


    # perform a move and get the state for that move
    # calculate the reward for the move
    # store the state and reward inside of a node

def calc_reward(state):
    return 1












# Testing
game = Game()
minimax = False
board = game.board
for x in range(50):
    if x % 2 == 0:
        game.board.turn = chess.WHITE
    else:
        game.board.turn = chess.BLACK
    move = min_max(game)
    game.board.push(move)
    print(move)
    print(game.board)