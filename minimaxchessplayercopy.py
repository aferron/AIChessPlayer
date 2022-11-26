from __future__ import annotations
from abc import ABC, abstractmethod
from aichessboard import AIChessBoard
import chess
from chess import Move
from chessplayer import ChessPlayer
from dataclasses import dataclass, field
import numpy as np
from typing import Any

DEPTH = 5
MIN_DEFAULT = 99999
MAX_DEFAULT = -99999
BACK_ROW_FOR_WHITE = 18374686479671623680
BACK_ROW_FOR_BLACK = 255


@dataclass(order=True)
class Node:
    reward:         int
    board:          int=field(compare=False)
    move:           AIChessBoard=field(compare=False)
    win_status:     Move=field(compare=False)
    max:            int=field(compare=False)
    min:            int=field(compare=False)
    parent:         Any=field(compare=False)

    def copy(self) -> Node:
        return Node(self.reward, self.board, self.move, self.win_status, self.min, self.max, self.parent)

# TODO: run through some trials to see how minimax is working with turn taking, minimizing, etc.
# TODO: check how ordering is done with whether minimizing or maximizing / how turns are taken
# TODO: make sure this works whether our player is white or black
# TODO: write tests for everything

class MinimaxPlayer(ChessPlayer):
    def __init__(self, depth: int) -> None:
        self.depth = depth
        self.__name = self.__class__.__name__ + " (depth:" + str(depth) + ")"

    def get_next_move(self, board: AIChessBoard) -> Move:
        return self.min_max(board=board, depth=self.depth)

    # Wrapper function for pre_order
    def min_max(self, board: AIChessBoard, depth: int) -> chess.Move:
        maximizer = board.turn
        root = Node(reward=0, board=board, move=None, win_status=None, min=0, max=0, parent=None)
        solution_node = self.pre_order(root=root, minimax=minimax, depth=depth, maximizer=maximizer)
        # print ("move selected:", solution_node.move)
        return solution_node.move


    # Preorder DFS of binary tree.
    def pre_order(self, root: Node, depth: int, maximizer: bool) -> Node:
        is_root = (root.board == board) # Check if this is the real root node

        early_exit = self.check_terminal_state(root=root, depth=depth)
        if early_exit != None:
            return early_exit

        children = self.unpack(root=root) # Unpack each move to see the states
        if children.size == 0: # No viable moves are left in this path.
            return root

        tree = []
        for child in children:
            child_node = self.pre_order(board=board, root=child, minimax=minimax, depth=depth - 1)
            """
            alpha beta pruning might go here - after opening
            a node and getting the reward value the
            loop can be broken. The lines below can be used.
            # if child_node.reward > root.max:
            #     root.max = child_node.reward
            # if child_node.reward < root.min:
            #     root.min = child_node.reward
            """
            tree.append(child_node)

        # Return a random move in the absence of heuristic difference
        if tree.count(tree[0]) == len(tree):
            choice = np.random.choice(tree)
            if not is_root:
                choice.move = root.move
            return choice

        # Why do we only maximize when it's white's turn?
        # Return Max if it's whites turn
        if minimax:
            max_tree = max(tree)
            if not is_root:
                max_tree.move = root.move
            return max(tree)

        else: # Return min if it's Black's turn
            min_tree = min(tree)
            if not is_root:
                min_tree.move = root.move
            return min(tree)


    # Unpack nodes into their child states
    def unpack(self,root: Node) -> np.array(Node):
        base_board = root.board
        legalmoves = np.array(list(root.board.legal_moves))
        nodes = np.empty(len(legalmoves), dtype=Move)
        win_status = 0 # This case is taken care of by recursive call
        for i, move in enumerate(legalmoves):
            board = base_board.copy()
            board.push(move)
            reward = self.calc_reward(board)
            nodes[i] = Node(
                reward=reward, 
                board=board, 
                move=move, 
                win_status=win_status, 
                min=MIN_DEFAULT, 
                max=MAX_DEFAULT, 
                parent=root
            )
        return nodes


    def calc_reward(self,board: AIChessBoard) -> int:
        # Integrate heuristics
        return 0


    def white_wins(self, board: AIChessBoard) -> bool:
        # The number below is a binary encoding for the chessboard.
        return BACK_ROW_FOR_WHITE & board.occupied_co[chess.WHITE] != 0


    def black_wins(self, board):
        # The number below is a binary encoding for the chessboard.
        return BACK_ROW_FOR_BLACK & board.occupied_co[chess.BLACK] != 0


    # Check if the state is an end state and return rewards if so
    def check_terminal_state(self, root: Node, depth: int) -> Node:
        # Return if we hit a terminal state
        if self.white_wins(board):
            # Not sure this gives the correct reward
            # Should be based on who's turn it is at the actual root
            reward = 10 if board.turn == chess.WHITE else -10
            return Node(
                reward=reward,
                board=root.board,
                move=root.move,
                win_status=1,
                min=MIN_DEFAULT,
                max=MAX_DEFAULT, 
                parent=root
            )
        elif self.black_wins(board):
            reward = 10 if board.turn == chess.BLACK else -10
            print("black gets reward")
            return Node(
                reward=reward,
                board=root.board,
                move=root.move,
                win_status=-1,
                min=MIN_DEFAULT,
                max=MAX_DEFAULT, 
                parent=root
            )
        elif depth <= 0:
            reward = 0
            return Node(
                reward=reward,
                board=root.board,
                move=root.move,
                win_status=-1,
                min=MIN_DEFAULT,
                max=MAX_DEFAULT, 
                parent=root
            )
        else:
            return None


    def get_name(self) -> str:
        return self.__name



simple_board_fen = '8/1p6/8/8/8/8/1p6/8'
board = AIChessBoard(simple_board_fen)
board.turn = chess.BLACK

print("turn:", board.turn)
minimax = MinimaxPlayer(depth=1)
minimax.get_next_move(board)
print("turn:", board.turn)
# move = Move('a2', 'a3')
# Node(reward=1, board=board, move=move, win_status=1, min=0, max=1, parent=None)
# print(AIChessBoard('P7/1ppppppp/8/8/8/8/1PPPPPPP/8'))
