from aichess import AIChess, Results
from chessplayer import ChessPlayer
from randomchessplayer import RandomChessPlayer
import numpy as np
import matplotlib.pyplot as plt
from minimaxchessplayer import MinimaxPlayer
from typing import List

class Main:
    def __plot_results(
        self,
        baseline: ChessPlayer, 
        testplayers: List[ChessPlayer], 
        iterations: int, 
        wins: list[int], 
        losses: list[int], 
        draws: list[int]
    ):
        title = 'Baseline: ' + baseline.get_name() + '\n' + str(iterations) + ' iterations per run'
        labels = [player.get_name() for player in testplayers]
        x = np.arange(len(labels))
        width = .15

        r1 = np.arange(len(labels))
        r2 = [x + width for x in r1]
        r3 = [x + width for x in r2]

        fig, ax = plt.subplots()
        rects1 = ax.bar(r1, wins, width, label='Test Player Wins')
        rects2 = ax.bar(r2, losses, width, label='Baseline Wins')
        rects3 = ax.bar(r3, draws, width, label='Draws')

        ax.set_ylabel('Percent Wins for Test Player')
        ax.set_xlabel('Player Type')
        ax.set_title(title)
        ax.set_xticks(x, labels)
        ax.legend()

        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)
        ax.bar_label(rects3, padding=3)
        fig.tight_layout()
        plt.savefig('charts/' + title)
        plt.show()
    
    def run(self):
        num_iterations = 50
        depth_iterations = [1, 2]
        wins, losses, draws = np.empty(len(depth_iterations)), np.empty(len(depth_iterations)), np.empty(len(depth_iterations))
        baseline = RandomChessPlayer()
        testplayers: List[ChessPlayer] = [MinimaxPlayer(depth=depth) for depth in depth_iterations]
        test_results: List[Results] = AIChess(iterations=num_iterations, baseline=baseline, testplayers=testplayers).run()
        for i, depth_test in enumerate(test_results):
            temp_wins, temp_losses, temp_draws = depth_test.percent_wins_player1, depth_test.percent_wins_player2, depth_test.percent_draws
            wins[i] = np.round(temp_wins, 2) * 100
            losses[i] = np.round(temp_losses, 2) * 100
            draws[i] = np.round(temp_draws, 2) * 100
        self.__plot_results(baseline, testplayers, num_iterations, wins, losses, draws)

Main().run()