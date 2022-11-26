from aichessboard import AIChessBoard
import chess
from chess import Move
from minimaxchessplayer import MinimaxPlayer, Node
import numpy as np

WINNING_BOARD_FOR_WHITE = 'P7/1ppppppp/8/8/8/8/1PPPPPPP/8'
WINNING_BOARD_FOR_BLACK = '8/1ppppppp/8/8/8/8/1PPPPPPP/p7'
NOT_WINNING_BOARD = '8/1ppppppp/8/8/8/8/1PPPPPPP/8'

class TestMinimaxChessPlayer:
    def test_node_creation(self) -> None:
        board = AIChessBoard()
        move = Move('a2', 'a3')
        node = Node(reward=1, board=board, move=move, win_status=1, min=0, max=1, parent=None)
        assert node.reward == 1

    def test_white_wins_when_white_is_on_back_row(self) -> None:
        board = AIChessBoard(WINNING_BOARD_FOR_WHITE)
        minimaxplayer = MinimaxPlayer(depth=1)
        assert minimaxplayer.white_wins(board=board) == True

    def test_white_wins_is_false_when_white_is_not_on_back_row(self) -> None:
        board = AIChessBoard(NOT_WINNING_BOARD)
        minimaxplayer = MinimaxPlayer(depth=1)
        assert minimaxplayer.white_wins(board=board) == False

    def test_black_wins_when_black_is_on_back_row(self) -> None:
        board = AIChessBoard(WINNING_BOARD_FOR_BLACK)
        minimaxplayer = MinimaxPlayer(depth=1)
        assert minimaxplayer.black_wins(board=board) == True

    def test_black_wins_is_false_when_black_is_not_on_back_row(self) -> None:
        board = AIChessBoard(NOT_WINNING_BOARD)
        minimaxplayer = MinimaxPlayer(depth=1)
        assert minimaxplayer.black_wins(board=board) == False

    def test_unpack_gives_an_array_of_nodes_with_legal_moves(self) -> None:
        board = AIChessBoard(NOT_WINNING_BOARD)
        minimaxplayer = MinimaxPlayer(depth=1)
        root = Node(
            reward=0,
            board=board,
            move=None,
            win_status=None,
            min=0,
            max=0,
            parent=None
        )
        unpacked_moves = {node.move for node in minimaxplayer.unpack(root=root)}

        assert unpacked_moves == set(board.legal_moves)

    def __check_reward(
        self, 
        player_turn: chess.Color, 
        board_fen: str, 
        player_wins: bool,
        player_loses: bool, 
        max_depth_reached: bool
    ) -> None:
        board = AIChessBoard(board_fen)
        board.turn = player_turn
        root = Node(
            reward=0,
            board=board,
            move=None,
            win_status=None,
            min=0,
            max=0,
            parent=None
        )
        minimaxplayer = MinimaxPlayer(depth=1)
        result_node = minimaxplayer.check_terminal_state(
            board=board, 
            root=root, 
            depth=0 if max_depth_reached else 1
        )

        if player_wins:
            assert result_node.reward == 10
        elif player_loses:
            assert result_node.reward == -10
        elif max_depth_reached:
            assert result_node.reward == 0
        else:
            assert result_node == None

    def test_check_terminal_state_returns_reward_if_white_is_maximizer_and_wins2(self) -> None:
        self.__check_reward(
            player_turn=chess.WHITE, 
            board_fen=WINNING_BOARD_FOR_WHITE,
            player_wins=True,
            player_loses=False,
            max_depth_reached=False
        )
        
    def test_negative_reward_returned_if_white_is_maximizer_and_loses(self) -> None:
        self.__check_reward(
            player_turn=chess.WHITE, 
            board_fen=WINNING_BOARD_FOR_BLACK,
            player_wins=False,
            player_loses=True,
            max_depth_reached=False
        )
        
    def test_check_terminal_state_returns_reward_if_black_is_maximizer_and_wins(self) -> None:
        self.__check_reward(
            player_turn=chess.BLACK, 
            board_fen=WINNING_BOARD_FOR_BLACK,
            player_wins=True,
            player_loses=False,
            max_depth_reached=False
        )
        
    def test_negative_reward_returned_if_black_is_maximizer_and_loses(self) -> None:
        self.__check_reward(
            player_turn=chess.BLACK, 
            board_fen=WINNING_BOARD_FOR_WHITE,
            player_wins=False,
            player_loses=True,
            max_depth_reached=False
        )
        
    def test_check_terminal_state_returns_no_reward_if_max_depth_reached(self) -> None:
        self.__check_reward(
            player_turn=chess.BLACK, 
            board_fen=NOT_WINNING_BOARD,
            player_wins=False,
            player_loses=False,
            max_depth_reached=True
        )
        
    def test_none_returned_if_not_terminal_state(self) -> None:
        self.__check_reward(
            player_turn=chess.BLACK, 
            board_fen=NOT_WINNING_BOARD,
            player_wins=False,
            player_loses=False,
            max_depth_reached=False
        )
        