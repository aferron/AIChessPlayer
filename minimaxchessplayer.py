from __future__ import annotations
from aichessboard import AIChessBoard
import chess
from chess import Move
from chessplayer import ChessPlayer
from heuristics import *
from dataclasses import dataclass, field
from enum import Enum
import numpy as np

REWARD_DEFAULT = 0
MIN_DEFAULT = 99999
MAX_DEFAULT = -99999
BACK_ROW_FOR_WHITE = 18374686479671623680
BACK_ROW_FOR_BLACK = 255

class WinReward(Enum):
    WIN = 10
    LOSS = -10
    DRAW = 0

class WinStatus(Enum):
    WIN = 1
    LOSS = -1
    DRAW = 0


# The fields max and min in Node can be used for AlphaBeta pruning
@dataclass(order=True)
class Node:
    reward_if_taking_best_move: int
    board:          AIChessBoard=field(compare=False)
    move_that_generated_this_board: Move=field(compare=False)
    best_move_from_board: Move=field(compare=False)
    win_status:     WinStatus=field(compare=False) 
    max:            int=field(compare=False)
    min:            int=field(compare=False)
    parent:         Node=field(compare=False)

    def copy(self) -> Node:
        return Node(
            self.reward_if_taking_best_move,
            self.board, 
            self.move_that_generated_this_board,
            self.best_move_from_board,
            self.win_status, 
            self.min, 
            self.max, 
            self.parent
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.reward_if_taking_best_move == other.reward_if_taking_best_move

class MinimaxPlayer(ChessPlayer):
    def __init__(self, depth: int, heuristics: List(Heuristic)) -> None:
        self.depth = depth
        self.heuristic_calculator = Heuristics(heuristics)
        self.__name = self.__class__.__name__ + " (depth:" + str(depth) + ")"

    def get_next_move(self, board: AIChessBoard) -> Move:
        return self.min_max(board=board, depth=self.depth)

    # Wrapper function for pre_order
    def min_max(self, board: AIChessBoard, depth: int) -> chess.Move:
        node_depth = depth + 1 #increment to let preorder decrement to the proper depth
        root = Node(
            reward_if_taking_best_move=REWARD_DEFAULT,
            board=board,
            move_that_generated_this_board=None,
            best_move_from_board=None,
            win_status=None,
            min=MIN_DEFAULT,
            max=MAX_DEFAULT,
            parent=None
        )
        solution_node = self.pre_order(root_board=board, current=root, depth=node_depth)
        best_move = solution_node.best_move_from_board
        if best_move == None:
            raise ChessPlayer.ChessPlayerException("No legal moves remain")
        return best_move


    # Preorder DFS of binary tree.
    def pre_order(self, root_board: AIChessBoard, current: Node, depth: int) -> Node:

        early_exit_reward = self.check_terminal_state(
            root=current, 
            depth=depth, 
            maximizer=root_board.turn
        )
        if early_exit_reward != None:
            current.reward_if_taking_best_move = early_exit_reward
            if early_exit_reward < 0:
                current.win_status = WinStatus.LOSS
            elif early_exit_reward > 0:
                current.win_status = WinStatus.WIN
            else:
                current.win_status = WinStatus.DRAW
            return current

        # Unpack each move to see the states
        children: np.array(Node) = self.unpack(root=current)
        # Check if no viable moves are left in this path
        if children.size == 0: 
            current.reward_if_taking_best_move = WinReward.DRAW.value
            return current

        tree = []
        for child in children:
            child_node = self.pre_order(root_board=root_board, current=child, depth=depth - 1)
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
            best_child: Node = np.random.choice(tree)
        # otherwise maximize or minimize depending on whose turn it is
        else:
            best_child: Node = max(tree) if (current.board.turn == root_board.turn) else min(tree)
        current.reward_if_taking_best_move = best_child.reward_if_taking_best_move
        current.best_move_from_board = best_child.move_that_generated_this_board
        return current


    # Unpack nodes into their child states
    def unpack(self,root: Node) -> np.array(Node):
        base_board: AIChessBoard = root.board
        legalmoves = np.array(list(root.board.legal_moves))
        nodes = np.empty(len(legalmoves), dtype=Move)
        for i, move in enumerate(legalmoves):
            board = base_board.copy()
            board.push(move)
            # this takes the place of current.board.turn = minimax in pre_order
            # push changes the board turn so this shouldn't be necessary
            board.turn = not base_board.turn
            reward = self.calc_reward(board)
            nodes[i] = Node(
                reward_if_taking_best_move=reward,
                board=board, 
                move_that_generated_this_board=move,
                best_move_from_board=None,
                win_status=None, # taken care of by recursive call
                min=MIN_DEFAULT, 
                max=MAX_DEFAULT, 
                parent=root
            )
        return nodes


    def calc_reward(self,board: AIChessBoard) -> int:
        heuristic_value = self.heuristic_calculator.return_heuristic_value(board)
        # print(heuristic_value)
        return heuristic_value



    def white_wins(self, board: AIChessBoard) -> bool:
        return BACK_ROW_FOR_WHITE & board.occupied_co[chess.WHITE] != 0


    def black_wins(self, board: AIChessBoard) -> bool:
        return BACK_ROW_FOR_BLACK & board.occupied_co[chess.BLACK] != 0


    # Check if the state is an end state and return rewards if so
    def check_terminal_state(self, root: Node, depth: int, maximizer: chess.Color) -> int:
        if self.white_wins(root.board):
            return WinReward.WIN.value if maximizer == chess.WHITE else WinReward.LOSS.value
        elif self.black_wins(root.board):
            return WinReward.WIN.value if maximizer == chess.BLACK else WinReward.LOSS.value
        elif depth <= 0:
            return self.calc_reward(root.board)
        else:
            return None


    def get_name(self) -> str:
        return self.__name
