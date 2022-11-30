from aichessboard import AIChessBoard
import chess
from chess import Move
from chessplayer import ChessPlayer
from minimaxchessplayer import MinimaxPlayer, Node, ALPHA_DEFAULT, BETA_DEFAULT
import numpy as np
import pytest
from heuristics import Heuristic, Heuristics

WINNING_BOARD_FOR_WHITE = 'P7/1ppppppp/8/8/8/8/1PPPPPPP/8'
WINNING_BOARD_FOR_BLACK = '8/1ppppppp/8/8/8/8/1PPPPPPP/p7'
NOT_WINNING_BOARD = '8/1ppppppp/8/8/8/8/1PPPPPPP/8'

class TestMinimaxChessPlayer:
    def test_node_creation(self) -> None:
        board = AIChessBoard()
        move = Move('a2', 'a3')
        node = Node(
            reward_if_taking_best_move=1,
            board=board, 
            move_that_generated_this_board=move,
            best_move_from_board=None,
            win_status=1, 
            alpha=0,
            beta=0,
            parent=None
        )
        assert node.reward_if_taking_best_move == 1

    def test_two_equal_nodes_evaluated_as_equal(self) -> None:
        board = AIChessBoard()
        move = Move('a2', 'a3')
        node1 = Node(
            reward_if_taking_best_move=1,
            board=board, 
            move_that_generated_this_board=move,
            best_move_from_board=None,
            win_status=1, 
            alpha=0,
            beta=0,
            parent=None
        )
        node2 = node1.copy()
        assert node1 == node2
 
    def test_unequal_nodes_evaluate_as_not_equal(self) -> None:
        board = AIChessBoard()
        move = Move('a2', 'a3')
        node1 = Node(
            reward_if_taking_best_move=1,
            board=board, 
            move_that_generated_this_board=move,
            best_move_from_board=None,
            win_status=1, 
            alpha=0,
            beta=0,
            parent=None
        )
        node2 = node1.copy()
        node2.reward_if_taking_best_move = 2
        assert node1 != node2

    def test_white_wins_when_white_is_on_back_row(self) -> None:
        board = AIChessBoard(WINNING_BOARD_FOR_WHITE)
        minimaxplayer = MinimaxPlayer(depth=1, heuristics=None, run_alpha_beta=False)
        assert minimaxplayer.white_wins(board=board) == True

    def test_white_wins_is_false_when_white_is_not_on_back_row(self) -> None:
        board = AIChessBoard(NOT_WINNING_BOARD)
        minimaxplayer = MinimaxPlayer(depth=1, heuristics=None, run_alpha_beta=False)
        assert minimaxplayer.white_wins(board=board) == False

    def test_black_wins_when_black_is_on_back_row(self) -> None:
        board = AIChessBoard(WINNING_BOARD_FOR_BLACK)
        minimaxplayer = MinimaxPlayer(depth=1, heuristics=None, run_alpha_beta=False)
        assert minimaxplayer.black_wins(board=board) == True

    def test_black_wins_is_false_when_black_is_not_on_back_row(self) -> None:
        board = AIChessBoard(NOT_WINNING_BOARD)
        minimaxplayer = MinimaxPlayer(depth=1, heuristics=None, run_alpha_beta=False)
        assert minimaxplayer.black_wins(board=board) == False

    def test_unpack_gives_an_array_of_nodes_with_legal_moves(self) -> None:
        board = AIChessBoard(NOT_WINNING_BOARD)
        minimaxplayer = MinimaxPlayer(depth=1, heuristics=[Heuristic], run_alpha_beta=False)
        root = Node(
            reward_if_taking_best_move=0,
            board=board,
            move_that_generated_this_board=None,
            best_move_from_board=None,
            win_status=None,
            alpha=0,
            beta=0,
            parent=None
        )
        unpacked_moves = {node.move_that_generated_this_board
                          for node in minimaxplayer.unpack(maximizer=board.turn, root=root, depth=1)}

        assert unpacked_moves == set(board.legal_moves)

    def __check_reward(
        self, 
        maximizer: chess.Color, 
        board_fen: str, 
        player_wins: bool,
        player_loses: bool, 
        max_depth_reached: bool
    ) -> None:
        board = AIChessBoard(board_fen)
        board.turn = maximizer
        root = Node(
            reward_if_taking_best_move=0,
            board=board,
            move_that_generated_this_board=None,
            best_move_from_board=None,
            win_status=None,
            alpha=0,
            beta=0,
            parent=None
        )
        minimaxplayer = MinimaxPlayer(depth=1, heuristics=[Heuristic], run_alpha_beta=False)
        result_reward = minimaxplayer.check_terminal_state(
            root=root, 
            depth=0 if max_depth_reached else 1,
            maximizer=maximizer
        )

        if player_wins:
            assert result_reward == 10
        elif player_loses:
            assert result_reward == -10
        elif max_depth_reached:
            assert result_reward == 0
        else:
            assert result_reward == None

    def test_check_terminal_state_returns_reward_if_white_is_maximizer_and_wins2(self) -> None:
        self.__check_reward(
            maximizer=chess.WHITE, 
            board_fen=WINNING_BOARD_FOR_WHITE,
            player_wins=True,
            player_loses=False,
            max_depth_reached=False
        )
        
    def test_negative_reward_returned_if_white_is_maximizer_and_loses(self) -> None:
        self.__check_reward(
            maximizer=chess.WHITE, 
            board_fen=WINNING_BOARD_FOR_BLACK,
            player_wins=False,
            player_loses=True,
            max_depth_reached=False
        )
        
    def test_check_terminal_state_returns_reward_if_black_is_maximizer_and_wins(self) -> None:
        self.__check_reward(
            maximizer=chess.BLACK, 
            board_fen=WINNING_BOARD_FOR_BLACK,
            player_wins=True,
            player_loses=False,
            max_depth_reached=False
        )
        
    def test_negative_reward_returned_if_black_is_maximizer_and_loses(self) -> None:
        self.__check_reward(
            maximizer=chess.BLACK, 
            board_fen=WINNING_BOARD_FOR_WHITE,
            player_wins=False,
            player_loses=True,
            max_depth_reached=False
        )
        
    def test_check_terminal_state_returns_no_reward_if_max_depth_reached(self) -> None:
        self.__check_reward(
            maximizer=chess.BLACK, 
            board_fen=NOT_WINNING_BOARD,
            player_wins=False,
            player_loses=False,
            max_depth_reached=True
        )
        
    def test_none_returned_if_not_terminal_state(self) -> None:
        self.__check_reward(
            maximizer=chess.BLACK, 
            board_fen=NOT_WINNING_BOARD,
            player_wins=False,
            player_loses=False,
            max_depth_reached=False
        )

    def test_pre_order_returns_best_move(self) -> None:
        board_fen = '8/1p1p4/8/8/8/5p2/1P1P4/8'
        best_move = Move.from_uci('f3f2')
        board = AIChessBoard(board_fen)
        board.turn = chess.BLACK
        node = Node(
            reward_if_taking_best_move=0,
            board=board,
            move_that_generated_this_board=None,
            best_move_from_board=None,
            win_status=None,
            alpha=ALPHA_DEFAULT,
            beta=BETA_DEFAULT,
            parent=None
        )
        minimaxplayer = MinimaxPlayer(depth=3, heuristics=[Heuristic], run_alpha_beta=False)
        result = minimaxplayer.pre_order(root_board=board, current=node, depth=minimaxplayer.depth)
        assert result.best_move_from_board == best_move
        
    def test_exception_thrown_if_no_moves_possible(self) -> None:
        board_fen = '8/1p1p4/1P1P4/8/8/8/8/8'
        board = AIChessBoard(board_fen)
        node = Node(
            reward_if_taking_best_move=0,
            board=board,
            move_that_generated_this_board=None,
            best_move_from_board=None,
            win_status=None,
            alpha=ALPHA_DEFAULT,
            beta=BETA_DEFAULT,
            parent=None
        )
        minimaxplayer = MinimaxPlayer(depth=3, heuristics=None, run_alpha_beta=False)
        with pytest.raises(ChessPlayer.ChessPlayerException):
            minimaxplayer.get_next_move(board=board)
        
    def test_get_next_move_returns_best_move(self) -> None:
        board_fen = '8/1p1p4/8/8/8/5p2/1P1P4/8'
        best_move = Move.from_uci('f3f2')
        board = AIChessBoard(board_fen)
        board.turn = chess.BLACK
        node = Node(
            reward_if_taking_best_move=0,
            board=board,
            move_that_generated_this_board=None,
            best_move_from_board=None,
            win_status=None,
            alpha=ALPHA_DEFAULT,
            beta=BETA_DEFAULT,
            parent=None
        )
        minimaxplayer = MinimaxPlayer(depth=3, heuristics=[Heuristic], run_alpha_beta=False)
        result = minimaxplayer.get_next_move(board=board)
        assert result == best_move

    def test_get_next_move_returns_best_move_when_turn_is_white(self) -> None:
        board_fen = '8/1p1p4/2P5/8/8/5p2/1P1P4/8'
        best_move = Move.from_uci('c6d7')
        board = AIChessBoard(board_fen)
        node = Node(
            reward_if_taking_best_move=0,
            board=board,
            move_that_generated_this_board=None,
            best_move_from_board=None,
            win_status=None,
            alpha=ALPHA_DEFAULT,
            beta=BETA_DEFAULT,
            parent=None
        )
        minimaxplayer = MinimaxPlayer(depth=3, heuristics=[0], run_alpha_beta=False)
        result = minimaxplayer.get_next_move(board=board)
        assert result == best_move

    def test_maximizer_is_correct_for_alpha_beta_pruning(self):
        board = AIChessBoard(NOT_WINNING_BOARD)
        root = Node(
            reward_if_taking_best_move=0,
            board=board,
            move_that_generated_this_board=None,
            best_move_from_board=None,
            win_status=None,
            alpha=ALPHA_DEFAULT,
            beta=BETA_DEFAULT,
            parent=None
        )
        maximizer = True if (root.board.turn == chess.WHITE) else False
        minimizer = True if (root.board.turn != chess.WHITE) else False
        assert maximizer is True and minimizer is False

    # This test needs fixed...
    def test_alpha_beta_pruning_returns_pruned_array_of_legal_moves(self) -> None:
        board = AIChessBoard(NOT_WINNING_BOARD)
        minimaxplayer = MinimaxPlayer(depth=1, heuristics=None, run_alpha_beta=False)
        root = Node(
            reward_if_taking_best_move=0,
            board=board,
            move_that_generated_this_board=None,
            best_move_from_board=None,
            win_status=None,
            alpha=ALPHA_DEFAULT,
            beta=BETA_DEFAULT,
            parent=None
        )
        legalmoves = np.array(list(root.board.legal_moves))
        nodes = np.empty(len(legalmoves), dtype=Move)
        base_board: AIChessBoard = root.board
        new_board = base_board.copy()
        new_board.push(legalmoves[0])
        new_board.turn = not base_board.turn

        nodes[0] = Node(
            reward_if_taking_best_move=0,
            board=board,
            move_that_generated_this_board=legalmoves[0],
            best_move_from_board=None,
            win_status=None,  # taken care of by recursive call
            alpha=root.alpha,
            beta=root.beta,
            parent=root
        )

        alpha_beta_moves = {node.move_that_generated_this_board for node in minimaxplayer.alpha_beta_pruning(
            max_player=False,
            value=root.alpha,
            children=nodes,
            child_index=0)}

        assert alpha_beta_moves < set(board.legal_moves)