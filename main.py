from aichess import AIChess, Results
from chessplayer import ChessPlayer
from heuristics import Heuristic
import matplotlib.pyplot as plt
import numpy as np
from minimaxchessplayer import MinimaxPlayer
from randomchessplayer import RandomChessPlayer
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
        title = 'Baseline: ' + baseline.get_name() + '\n' + str(iterations) + \
            ' iterations per run'
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

        ax.set_ylabel('Percent Wins or Draws')
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

    def __append_as_percent(self, results_by_type: np.array[float], percent: float) -> None:
        results_by_type.append(np.round(percent, 2) * 100)
    
    def run(self):
        num_iterations = 50
        depth_iterations = [1, 2, 3]
        baselines =  [
            MinimaxPlayer(
                depth=depth, 
                heuristics=[
                    Heuristic.Distance_From_Starting_Location, 
                    Heuristic.Maximize_Number_Of_Pieces
                ]
            ) for depth in depth_iterations
        ]
        testplayers = [
            MinimaxPlayer(
                depth=depth, 
                heuristics=[
                    Heuristic.Piece_Could_Be_Captured, 
                    Heuristic.Distance_From_Starting_Location, 
                    Heuristic.Keep_Pawns_Diagonally_Supported, 
                    Heuristic.Stacked_Pawns, 
                    Heuristic.Maximize_Number_Of_Pieces
                ]
            ) for depth in depth_iterations
        ]
        test_results: List[List[Results]] = AIChess(iterations=num_iterations, baselines=baselines, testplayers=testplayers).run()
        for results_per_baseline in enumerate(test_results):
            test_player_wins, baseline_wins, draws = [], [], []
            for results in results_per_baseline:
                # test_player_win_percent, baseline_win_percent, draw_percent = results.percent_wins_player1, results.percent_wins_player2, results.percent_draws
                self.__append_as_percent(results_by_type=test_player_wins, percent=results.percent_wins_player1)
                self.__append_as_percent(results_by_type=baseline_wins, percent=results.percent_wins_player2)
                self.__append_as_percent(results_by_type=draws, percent=results.percent_draws)
                
                # test_player_wins.append(np.round(temp_wins, 2) * 100)
                # baseline_wins.append( np.round(temp_losses, 2) * 100)
                # draws.append( np.round(temp_draws, 2) * 100)
            self.__plot_results(results_per_baseline, testplayers, num_iterations, test_player_wins, baseline_wins, draws)

Main().run()
