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
    max:            Any=field(compare=False)
    min:            Any=field(compare=False)
    parent:          Any=field(compare=False)

    def __init__(self, reward, board, move, win_status, min, max, parent):
        self.reward = reward
        self.board = board
        self.move = move
        self.win_status = win_status
        self.min = min
        self.max = max
        self.parent = parent
    def copy(self):
        return Node(self.reward, self.board, self.move, self.win_status, self.min, self.max, self.parent)



def min_max(game, depth):
    board = game.board
    # The line below toggles the current player opposite for the wrapper function.
    minimax = not game.board.turn
    node_depth = depth + 1 #increment to let preorder decrement to the proper depth
    root = Node(0, board, None, None, 0, 0, None)
    solution_node = pre_order(game,root, minimax, node_depth)
    return solution_node.move

# Preorder DFS of binary tree.
def pre_order(game, root, minimax, depth):
    max_default = -9999
    min_default = 9999
    depth -= 1
    minimax = (minimax == False) # This will switch max and min on each call
    black_wins = 255  & root.board.occupied_co[chess.BLACK] != 0
    white_wins = 18374686479671623680 & root.board.occupied_co[chess.WHITE] != 0
    root_copy = root.copy() # Can set the current turn without changing parent
    root_copy.board.turn = minimax # Set whose turn it is
    is_root = root.board == game.board # Check if this is the real root node


    # Return if we hit a terminal state
    if white_wins:
        reward = 10 if game.board.turn == chess.WHITE else -10
        return Node(reward,root_copy.board,root_copy.move,-1,min_default,max_default, root)
    if black_wins:
        reward = 10 if game.board.turn == chess.BLACK else -10
        return Node(reward,root_copy.board,root_copy.move,1,min_default,max_default, root)
    if depth <= 0:
        reward = 0
        return Node(reward,root_copy.board,root_copy.move,-1,min_default,max_default, root)


    children = unpack(root_copy) # we have the child nodes and their state
    if children == []: # No viable moves left. Stalemate down this path.
        return root_copy

    tree = list()
    for child in children:
        child_node = pre_order(game, child, minimax, depth)

        """
        alpha beta pruning might go here - after opening
        a node and getting the reward value the
        loop can be broken.
        """
        if child_node.reward > root.max:
            root.max = child_node.reward
        if child_node.reward < root.min:
            root.min = child_node.reward

        tree.append(child_node)

        """
        # This can be used to have an agent immediately go for victory
        # if it's found down a path.
        """
        # if child_node.win_status == 1:
        #     if root.board == game.board: #checking if this is the original root
        #         return child_node
        #     else:
        #         # if the game is over, then return the move to get here to root.
        #         temp = Node(1,root_copy.board,root_copy.move,1, min_default, max_default, root)
        #         return temp


    # return a random move in the absense of heuristic difference
    if tree.count(tree[0]) == len(tree):
        choice = np.random.choice(tree)
        if not is_root:
            choice.move = root.move
        return choice

    if minimax == True: # Whites turn
        max_tree = max(tree)
        if not is_root:
            max_tree.move = root.move
        return max(tree)

    else: # Blacks turn
        min_tree = min(tree)
        if not is_root:
            min_tree.move = root.move
        return min(tree)


def unpack(root):
    max_default = -9999
    min_default = 9999
    base_board = root.board
    legalmoves = list(root.board.legal_moves)
    nodes = []
    for move in legalmoves:
        board = base_board.copy()
        board.push(move)
        reward = calc_reward(board)
        win_status = 0 # This case is taken care of by recursive call
        nodes.append(Node(reward, board, move, win_status,min_default,max_default, root))
    return nodes


def calc_reward(state):
    return 0


# Testing
game = Game()
minimax = False
for x in range(50):
    if x % 2 == 0:
        game.board.turn = chess.WHITE
    else:
        game.board.turn = chess.BLACK
    move = min_max(game, 4)
    if move == None:
        break
    game.board.push(move)
    print(move)
    print(game.board)