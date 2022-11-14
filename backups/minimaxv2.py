from  abc import ABC, abstractmethod
from aichessboard import AIChessBoard
from chess import Move
from dataclasses import dataclass, field
from typing import Any
import chess
import numpy as np
from chessplayer import ChessPlayer

DEPTH = 3
MAX_DEFAULT = -99999
MIN_DEFAULT = 99999

@dataclass(order=True)
class Node:
    reward:         int
    board:          Any=field(compare=False)
    move:           Any=field(compare=False)
    win_status:     Any=field(compare=False)
    max:            Any=field(compare=False)
    min:            Any=field(compare=False)
    parent:         Any=field(compare=False)

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


class minimaxPlayer(ChessPlayer):

    def get_next_move(self, board: AIChessBoard) -> Move:
        return self.min_max(board, DEPTH)

    def min_max(self, board: AIChessBoard, depth: int) -> chess.Move:
        board_1 = board
        # The line below toggles the current player opposite for the wrapper function.
        minimax = not board_1.turn
        node_depth = depth + 1 #increment to let preorder decrement to the proper depth
        root = Node(0, board, None, None, 0, 0, None)
        solution_node = self.pre_order(board_1, root, minimax, node_depth)
        return solution_node.move

        # Preorder DFS of binary tree.
    def pre_order(self, board: AIChessBoard, root: Node, minimax: bool, depth: int) -> Node:
        depth -= 1
        minimax = (minimax == False) # This will switch max and min on each call
        root.board.turn = minimax # Set whose turn it is
        is_root = root.board == board # Check if this is the real root node

        # Return if we hit a terminal state
        if self.white_wins(board):
            reward = 10 if board.turn == chess.WHITE else -10
            return Node(reward,root.board,root.move,-1,MIN_DEFAULT,MAX_DEFAULT, root)
        if self.black_wins(board):
            reward = 10 if board.turn == chess.BLACK else -10
            return Node(reward,root.board,root.move,1,MIN_DEFAULT,MAX_DEFAULT, root)
        if depth <= 0:
            reward = 0
            return Node(reward,root.board,root.move,-1,MIN_DEFAULT,MAX_DEFAULT, root)

        children = self.unpack(root) # we have the child nodes and their state
        if children == []: # No viable moves left. Stalemate down this path.
            return root

        tree = list()
        for child in children:
            child_node = self.pre_order(board, child, minimax, depth)

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


    def unpack(self,root):
        base_board = root.board
        legalmoves = np.array(root.board.legal_moves)
        nodes = np.empty(len(legalmoves), dtype=Move)
        for i, move in enumerate(legalmoves):
            board = base_board.copy()
            board.push(move)
            reward = self.calc_reward(board)
            win_status = 0 # This case is taken care of by recursive call
            nodes[i] = Node(reward, board, move, win_status,MIN_DEFAULT,MAX_DEFAULT, root)
        return nodes


    def calc_reward(self,state):
        # Integrate heuristics
        return 0

    def white_wins(self, board):
        return 18374686479671623680 & board.occupied_co[chess.WHITE] != 0

    def black_wins(self, board):
        return 255 & board.occupied_co[chess.BLACK] != 0