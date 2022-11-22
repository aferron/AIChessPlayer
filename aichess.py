from game import Game
from randomchessplayer import RandomChessPlayer
from minimaxchessplayer import minimaxPlayer
import numpy as np
import matplotlib.pyplot as plt

class AIChess:
    def __init__(self, iterations: int, visual: bool, verbose: bool, depth: int) -> None:
        self.__iterations: int = iterations
        self.__visual: bool = visual
        self.__verbose: bool = verbose
        self.__percent_wins_player1: float = 0.0
        self.__percent_wins_player2: float = 0.0
        self.__percent_draws: float = 0.0
        self.__depth = depth

    # TODO: Build up more structure/abstractions to evaluate various player types
    def run(self):
        player1_wins = 0
        draws = 0
        for i in range(self.__iterations):
            # This is for testing until player type is incorporated into the class.
            player1 = minimaxPlayer(self.__depth)
            # player1 = RandomChessPlayer()
            player2 = RandomChessPlayer()
            game = Game(
                white=player1,
                black=player2,
                visual=self.__visual,
                verbose=self.__verbose
            )

            winner = game.run()
            if winner is None:
                draws += 1

            # If winner is True, white won (player1)
            elif winner:
                player1_wins += 1

        self.__percent_wins_player1 = player1_wins / self.__iterations
        self.__percent_draws = draws / self.__iterations
        self.__percent_wins_player2 = 1 - (self.__percent_wins_player1 + self.__percent_draws)
        print("player 1 win percent:", self.__percent_wins_player1)
        print("player 2 win percent:", self.__percent_wins_player2)
        print("draws percent:", self.__percent_draws)
        print("number iterations:", self.__iterations)
        return self.__percent_wins_player1, self.__percent_wins_player2, self.__percent_draws

        # How to use:
        # AIChess(iterations=10, visual=False, verbose=False, depth=1).run()