from aichess import AIChess, Results
from chessplayer import ChessPlayer
from heuristics import Heuristic
import matplotlib.pyplot as plt
import numpy as np
from minimaxchessplayer import MinimaxPlayer
from randomchessplayer import RandomChessPlayer
from typing import List

class Main:
    def run(self) -> None:
        self.__run_minimax_with_heuristics_vs_random()

    def __run_and_plot_one_experiment(self, iterations: int, baselines: List[ChessPlayer], testplayers: List[ChessPlayer]) -> None:
        test_results: List[List[Results]] = AIChess(iterations=iterations, baselines=baselines, testplayers=testplayers).run()
        print("test_results: ", test_results)
        for i, results_per_baseline in enumerate(test_results):
            baseline = baselines[i]
            print ("results_per_baseline:", results_per_baseline)
            test_player_wins, baseline_wins, draws = [], [], []
            for results in results_per_baseline:
                print("results: ", results)
                self.__append_as_percent(results_by_type=test_player_wins, percent=results.percent_wins_player1)
                self.__append_as_percent(results_by_type=baseline_wins, percent=results.percent_wins_player2)
                self.__append_as_percent(results_by_type=draws, percent=results.percent_draws)
            self.__plot_results(
                baseline=baseline,
                testplayers=testplayers,
                iterations=iterations, 
                wins=test_player_wins, 
                losses=baseline_wins, 
                draws=draws
                )

    def __append_as_percent(self, results_by_type: np.array(float), percent: float) -> None:
        results_by_type.append(np.round(percent, 2) * 100)

    def __plot_results(
        self,
        baseline: ChessPlayer, 
        testplayers: List[ChessPlayer], 
        iterations: int, 
        wins: list[int], 
        losses: list[int], 
        draws: list[int]
    ) -> None:
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

    def __run_heuristics_by_depth_experiments(self) -> None:
        num_iterations = 5
        depth_iterations = [1, 2, ]
        baselines =  [MinimaxPlayer(
            depth=depth, 
            heuristics=[Heuristic.Distance_From_Starting_Location, Heuristic.Maximize_Number_Of_Pieces],
            run_alpha_beta=True) \
                for depth in depth_iterations]
        testplayers = [
            MinimaxPlayer(
                depth=depth, 
                heuristics=[
                    Heuristic.Piece_Could_Be_Captured, 
                    Heuristic.Distance_From_Starting_Location, 
                    Heuristic.Keep_Pawns_Diagonally_Supported, 
                    Heuristic.Stacked_Pawns, 
                    Heuristic.Maximize_Number_Of_Pieces
                ],
                run_alpha_beta=True
            ) for depth in depth_iterations]
        self.__run_and_plot_one_experiment(iterations=num_iterations, baselines=baselines, testplayers=testplayers)

    def __run_heuristics_ablation_study(self) -> None:
        num_iterations = 10
        depth = 3
        all_heuristics = list(Heuristic)
        baselines =  [MinimaxPlayer(depth=depth, heuristics=[], run_alpha_beta=False), MinimaxPlayer(depth=depth, heuristics=all_heuristics, run_alpha_beta=True)]
        testplayers = [MinimaxPlayer(depth=depth, heuristics=[heuristic], run_alpha_beta=True) for heuristic in all_heuristics] + \
            [MinimaxPlayer(depth=depth, heuristics=[heuristic for heuristic in all_heuristics if all_heuristics.index(heuristic) != index], run_alpha_beta=False) for index in range(len(all_heuristics))]
        self.__run_and_plot_one_experiment(iterations=num_iterations, baselines=baselines, testplayers=testplayers)

    def __run_minimax_with_heuristics_vs_random(self) -> None:
        num_iterations = 100
        baselines = [RandomChessPlayer()]
        testplayers = [MinimaxPlayer(depth=depth, heuristics=list(Heuristic), run_alpha_beta=False) for depth in range(4)]
        self.__run_and_plot_one_experiment(iterations=num_iterations, baselines=baselines, testplayers=testplayers)

Main().run()

