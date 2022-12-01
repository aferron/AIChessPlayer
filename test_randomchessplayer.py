from aichessboard import AIChessBoard
from randomchessplayer import RandomChessPlayer
from unittest.mock import MagicMock
import time


class TestRandomChessPlayer:
    board = AIChessBoard('8/pppppppp/8/8/8/8/PPPPPPPP/8')

    def test_time_is_correctly_averaged(self) -> None:
        time.process_time = MagicMock()
        time.process_time.side_effect = iter([0, 1, 0, 0.25, 0, 1.75])
        player = RandomChessPlayer(time)
        for i in range(3):
            player.get_next_move(self.board)

        assert player.average_time_to_get_move == 1.0